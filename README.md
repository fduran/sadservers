# SadServers

## What

[SadServers](https://sadservers.com/) is a SaaS where users can test their Linux troubleshooting skills on real Linux servers in a "Capture the Flag" fashion.  

There's a collection of scenarios, a description of what's wrong and a test to check if the issue has been solved. The servers are spun up on the spot, users get an SSH shell via a browser window to an ephemeral server (destroyed after the alloted time for solving the challenge) and then they can try and solve the problem.  

Problems include common software that run on Linux, like databases or web servers although knowledge of the details for the specific application is not necessarily required. It also includes scenarios where you do need to be familiar with the technology with the issue, for example, a Docker scenario. The scenarios are for the most part real-world ones, as in they are similar to issues that we have encountered.

SadServers is aimed primarily at users that are professional Software Developers (possibly), System Administrators, DevOps engineers, SREs, and related positions that require server debugging and troubleshooting skills.  

Particularly SadServers wants to test these professionals (or people aspiring to these jobs) in a way that would be useful for the purpose of a troubleshooting part of a job interview.

## Why

To scratch a personal itch and because there's nothing like this that I'm aware of. There are/were some sandbox solutions like Katacoda (shut down in May 2022) but nothing that gives you a specific problem with a condition of victory on a real server.  

It's also my not-so-secret hope that a sophisticated enough version of SadServers could be used by tech companies (or for companies that carry on job interviews on their behalf) to automate or facilitate the Linux troubleshooting interview section.  

An annoyance I found during my interviews is that sometimes instead of helping, the interviewer unintentionally misleads you, or you feel like you are in a tv game where you have to maximize for some arbitrary points and come up with an game strategy that doesn't reflect real incident situations (do I try to keep solving this problem or do I move to the next one, which one is better?).

## How does it look?

![ux](sadservers_ux_medium.png)


## Architecture

See diagram:

![architecture](sadservers_architecture.jpg)

Users interact via HTTPS only with a web server and a proxy server connecting to the scenario VMs. The rest of the communications are internal between VPCs or AWS services. Each scenario VM reside in a VPC with no Internet-facing incoming access and limited egress access.

### Web server

The website is powered by [Django](https://www.djangoproject.com/) and Python3, with [Bootstrap](https://getbootstrap.com/) and plain Javascript at the front.  

In front of Django there's an [Nginx](https://www.nginx.com/) server and [Gunicorn](https://gunicorn.org/) WSGI server. The SSL certificate is generously provided by [Let's Encrypt](https://letsencrypt.org/) and its certbot, the best thing to happen to the Internet since Mosaic.

### Task Queue

New server requests are queued and processed in the background. On the front-end I'm using [Celery Progress Bar for Django](https://github.com/czue/celery-progress). The tasks are managed asynchronously by [Celery](https://docs.celeryq.dev/en/stable/) with a [RabbitMQ](https://www.rabbitmq.com/) back-end and with task results saved to the main database (and yes, maybe there should be a simpler but still robust stack instead of this).  

### Permanent Storage

A [PostgreSQL](https://www.postgresql.org/) database is the permanent storage backend, the first choice for RDBMS. [SQLite](https://www.sqlite.org/index.html) is a valid alternative for sites without a high rate of (concurrent) writes.  

Instances are requested on AWS using [Boto3](https://github.com/boto/boto3), based on scenario images. A Celery beat scheduler checks for expired instances and kills them.  

### Proxy Server

In the initial proof of concept, I had the users connect to the VMs public IP directly. For security reasons like terminating SSL, being able to use rate limiting, logging access and specially having the VMs with private IPs only, it's a good idea to route access to the scenario instances through a reverse web proxy server.  

Since the scenario instances are created on demand (at least some of them), I needed a way to dynamicaly inject in the web server configuration the route mappings, ie, using code against an API to configure the web server and reloading it. The configuration for proxying a VM would be like proxy.sadservers.com:port/somestring -> (proxy passes to upstream server) -> VM ip address:port .  (Using a path string is an option, other options could be passing a ...?parameter in the URL or in the HTTP headers). 

This was an interesting learning experience since unlike the rest of the stack I've never had this situation before. After considering some alternatives, I almost made it work with [Traefik](https://doc.traefik.io/traefik/) but I hit a wall, didn't seem to be a good solution for this case. and I discarded it.  A friend of mine suggested to use [Hashicorp Consul](https://www.consul.io/), where the Django server connects to and writes to its key/value store, and [Consul-template](https://github.com/hashicorp/consul-template), which monitors Consul and writes the key/values (string and IP) into Nginx configuration (which does the actual SSL and proxying) and reloads it. After figuring out production settings (certificates, tokens) it turned out to work very well.

### Scenario Instances

On the VM instances, [Gotty](https://github.com/yudai/gotty) provides a terminal with a shell as HTTP(S). An agent built with Golang and [Gin](https://github.com/gin-gonic/gin) provides a rest API to the main server, so solutions can be checked and commands can be sent to the scenario instance or data extracted from it.

### Other Infrastructure & Services

Without a lot of detail, there's quite a bit of auxiliary services needed to run a public service in a decent "production-ready" state. This includes notification services (AWS SES for email for example), logging service, external uptime monitoring service, scheduled backups, error logging (like [Sentry](https://sentry.io/)), infrastructure as code (Hashicorop [Terraform](https://www.terraform.io/) and [Packer](https://www.packer.io/)).


## User Experience

Not a UX expert as anyone can see but just trying to make it as simple and less confusing as possible.

## Code

This project may become Open Source at some point but for now the code is not publicly available. One reason is that showing the solution to the scenarios defeats the purpose and another reason is to expose details of how things are set up for security reasons. I'll be happy to chat about technical aspects of the project if someone is curious.

## Issues

- Opening a new scenario while one is ongoing will invalidate the session of the first one. Clues are based on sessions so the clues displayed will be that of the latest session, which will be incorrect for previous scenarios.  

## Roadmap

- Registering users.
- Timing solutions (this will allow to show a leaderboard).
- Multi-VM scenarios (troubleshooting Kubernetes for example).
- HTTPS for the agent. (a smart person could reverse-engineer and replace it ahem)
- Save & replay user command history.
- OS package repository cache/proxy server.

## Contact

Any feedback is appreciated, please email info@sadservers.com

## Collaboration

If you want to create a scenario, these are broadly the requirements:  

- A clear (not ambiguous) problem statement, ideally one that can be shown with a command or combination of commands.  
- Even more importantly, a clear pass/fail test for the user that they can run in the form of a command or commands and therefore it can be checked with a Bash script, i. e., if we run a check.sh script, it will always return a binary result (strings "OK" and "NO" for example). 
- A description of one solution to the problem, favoring simple and "production" ones.  
- An automated way to create the problem. This is, a script and other files that will set up the problem fully on a non-licenced Linux distribution available in AWS (for example, latest Debian or Ubuntu). For instance, if the scenario issue is about a broken web server configuration, the script would install the web server and replace the original config file with the problematic one.  A Hashicorp Packer template and auxiliary files would be even better :-) 
- Optionally, a set of clues or tips that will increasingly get the user closer to the solution.  
- Other:
    - I'm using ports :8080 and :6767 for the shell-to-web and agent, so don't use those ports.
    - Currently only supporting one VM scenarios and not multiple VM scenarios.
    - VMs should be fully self-contained and not need the Internet for anything, ie, the user wouldn't need to initiate connections from the scenario VM to the Internet save for ICMP (ping) and DNS traffic. A possible exception would be access to an OS package repository proxy. 


