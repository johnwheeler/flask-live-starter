# startup-starter

Go from 0 to 100 MPH with the infrastructure behind the Python web app in [From Google Form to $1000 in revenue in one month](https://blog.oldgeekjobs.com/from-google-form-to-1000-in-revenue-in-one-month-3f5cd75b6089).

This is a work in progress. It'll be ready to rock in less than a week. Stay tuned!

* Flask
* Gunicorn
* Nginx
* Postgresql

```
vagrant up
fab provision --hosts 192.168.33.10 --user vagrant -i .vagrant/machines/default/virtualbox/private_key
fab deploy --hosts 192.168.33.10 --user vagrant -i .vagrant/machines/default/virtualbox/private_key
fab configure --hosts 192.168.33.10 --user vagrant -i .vagrant/machines/default/virtualbox/private_key
```
