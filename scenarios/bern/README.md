# "Bern": Docker web container can't connect to db container.

## Description

There are two Docker containers running, a web application (Wordpress or WP) and a database (MariaDB) as back-end, but if we look at the web page, we see that it cannot connect to the database.
<kbd>curl -s localhost:80 |tail -4</kbd> returns:<br><br>
<code>
&lt;body id="error-page"&gt;
	&lt;div class="wp-die-message">&lt;h1&gt;Error establishing a database connection&lt;/h1&gt;&lt;/div&gt;&lt;/body&gt;
&lt;/html&gt;
<br><br>
</code>
This is not a Wordpress code issue (the image is :latest with some network utilities added). What you need to know is that WP uses "WORDPRESS_DB_" environment variables to create the MySQL connection string. See the ./html/wp-config.php WP config file for example (from /home/admin).<br><br>

## Test

<kbd>sudo docker exec wordpress mysqladmin -h mysql -u root -ppassword ping</kbd> . The wordpress container is able to connect to the database in the mariadb container and returns <kbd>mysqld is alive</kbd>.

<b>check.sh</b>

```
#!/usr/bin/bash
res=$(sudo docker exec wordpress mysqladmin -h mysql -u root -ppassword --connect-timeout 2 ping)
res=$(echo $res|tr -d '\r')

if [[ "$res" = "mysqld is alive" ]]
then
  echo -n "OK"
else
  echo -n "NO"
fi
```

## Clues

<b>1. </b>We can connect to the database with "root:password" as username:password authentication:  `mysql -h 127.0.0.1 -u root -ppassword`<br>
We can get the user/password values from the database environment variables that we can see with <kbd>docker inspect mariadb</kbd><bt><br>
Try and see how you can connect in a similar way from the worpress container.<br><br>

<b>2. </b>Compare the database env vars that exist in the WP container from the ones that are needed, for ex <kbd>docker exec wordpress env |grep WORDPRESS_DB_</kbd> versus <kbd>grep WORDPRESS_DB_ ./html/wp-config.php</kbd> or <kbd>docker exec wordpress grep WORDPRESS_DB_ /var/www/html/wp-config.php</kbd><br><br>

<b>3. </b>From the previous hint, the username and password are correctly set, so WORDPRESS_DB_HOST or WORDPRESS_DB_NAME can be the culprits. from the 1st tip we can see if the WORDPRESS_DB_NAME is the default one in code "wordpress".<br><br>

<b>4. </b>The default database host for WP WORDPRESS_DB_HOST is "mysql", but this host is not defined, does not reach the mariadb container.<br><br>
<b>5. Solution: </b>There are several solutions. One is to define WORDPRESS_DB_HOST as Docker's IP 172.17.0.1 or the host's IP since the database container is exposing its port.