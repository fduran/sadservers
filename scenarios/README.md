# SadServers Scenarios

You can reproduce the SadServer scenarios included here using a target existing server (Debian 11 for example) and configuration automation tooling like Ansible or Packer.

Ansible is easier and faster to work with and recommended unless you want a server image as a result.

The resulting servers or images are different from the ones in SadServers in:
- They won't have the SadServer agent, but you don't need it. Almost all the agent does is to call the ~/agent/check.sh script to verify the solution, but you can call it yourself (returns "OK" or "NO").
- The shell-to-web utility, but you don't need it.

## Ansible

Basically, execute the Ansible playbook in the `ansible` directory of the scenario.  

For example: `ansible-playbook playbook-debian.yml -u admin -i "$ip,"`.

Here `-u admin` means to log in as admin user, this would be for example `-u ubuntu` in Ubuntu distros.  

There is no inventory file provided, you can add one or pass the hostname or ip address of the target server with the `-i` option (to confuse things, -i can also be used for the private key path, which can also be passed as `--private-key=/path/to/private/key`).

## Packer

The Hashicorp Packer template is specific for AWS and you'll need to provide the parameters in the `variables.pkr.hcl` file; namely:
-  the `source_ami` to use as a base (find latest Debian 11 for example) and - the AWS `region` for this image and the temporal VM and result image.

The temporary VM instance that Packer creates needs to be somewhere specific, so we need to pass a `vpc_id` and a `subnet_id` (or you can use the `default` VPC).

## Scenarios

[Scenario 1. "Saint John": what is writing to this log file?](scenario-1-saintjohn)
