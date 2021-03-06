..
    Copyright 2013 Hewlett-Packard Development Company, L.P.

    Licensed under the Apache License, Version 2.0 (the "License"); you may
    not use this file except in compliance with the License. You may obtain
    a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
    License for the specific language governing permissions and limitations
    under the License.

.. _devstack:

========
DevStack
========

The Designate team maintains a fork of devstack with Designate integration.

Instructions
++++++++++++

1. Get a clean Ubuntu 12.04 VM. DevStack "takes over". Don't use your desktop!

2. Clone Designate and DevStack inside the VM::

   $ git clone https://git.openstack.org/cgit/openstack-dev/devstack.git
   $ git clone https://github.com/openstack/designate.git

3. Install the Designate extension for DevStack::

   $ cd devstack
   $ ../designate/contrib/devstack/install.sh

4. Create a `localrc` config file::

       ADMIN_PASSWORD=password
       MYSQL_PASSWORD=password
       RABBIT_PASSWORD=password
       SERVICE_PASSWORD=password
       SERVICE_TOKEN=tokentoken

       # Just the basics to start with!
       ENABLED_SERVICES=rabbit,mysql,key

       # Enable core Designate services
       ENABLED_SERVICES+=,designate,designate-api,designate-central

       # Optional Designate services
       #ENABLED_SERVICES+=,designate-sink

       # ** Everything below is optional ***

       # Enable Horizon with Designate integration (needs nova)
       #ENABLED_SERVICES+=,horizon
       #HORIZON_REPO=git://github.com/moniker-dns/horizon.git
       #HORIZON_BRANCH=designate

       # Enable Nova (needs glance)
       #ENABLED_SERVICES+=,n-api,n-crt,n-obj,n-cpu,n-net,n-cond,n-sch
       #IMAGE_URLS+=",https://launchpad.net/cirros/trunk/0.3.0/+download/cirros-0.3.0-x86_64-disk.img"

       # Enable Glance
       #ENABLED_SERVICES+=,g-api,g-reg

5. Run DevStack::

   $ ./stack.sh

6. Enter the screen sessions "shell" window::

   $ ./rejoin-stack.sh

   Then press Ctrl+A followed by 0

7. Load credentials into the shell::

   $ source openrc admin admin # For the admin user, admin tenant
   $ source openrc admin demo  # For the admin user, demo tenant
   $ source openrc demo demo   # For the demo user, demo tenant

8. Try out the designate client::

       $ designate domain-create --name example.net. --email kiall@hp.com
       +------------+--------------------------------------+
       | Field      | Value                                |
       +------------+--------------------------------------+
       | name       | example.net.                         |
       | created_at | 2013-07-12T13:36:03.110727           |
       | updated_at | None                                 |
       | id         | 1fb5d17c-efaf-4e3c-aac0-482875d24b3e |
       | ttl        | 3600                                 |
       | serial     | 1373636163                           |
       | email      | kiall@hp.com                         |
       +------------+--------------------------------------+

       $ designate record-create 1fb5d17c-efaf-4e3c-aac0-482875d24b3e --type A --name www.example.net. --data 127.0.0.1
       +------------+--------------------------------------+
       | Field      | Value                                |
       +------------+--------------------------------------+
       | name       | www.example.net.                     |
       | data       | 127.0.0.1                            |
       | created_at | 2013-07-12T13:39:51.236025           |
       | updated_at | None                                 |
       | id         | d50c21d0-a13c-48e2-889e-0b9852a05acb |
       | priority   | None                                 |
       | ttl        | None                                 |
       | type       | A                                    |
       | domain_id  | 1fb5d17c-efaf-4e3c-aac0-482875d24b3e |
       +------------+--------------------------------------+

       $ designate record-list 1fb5d17c-efaf-4e3c-aac0-482875d24b3e
       +--------------------------------------+------+------------------+
       | id                                   | type | name             |
       +--------------------------------------+------+------------------+
       | d50c21d0-a13c-48e2-889e-0b9852a05acb | A    | www.example.net. |
       +--------------------------------------+------+------------------+

       $ designate record-get 1fb5d17c-efaf-4e3c-aac0-482875d24b3e d50c21d0-a13c-48e2-889e-0b9852a05acb
       +------------+--------------------------------------+
       | Field      | Value                                |
       +------------+--------------------------------------+
       | name       | www.example.net.                     |
       | data       | 127.0.0.1                            |
       | created_at | 2013-07-12T13:39:51.000000           |
       | updated_at | None                                 |
       | id         | d50c21d0-a13c-48e2-889e-0b9852a05acb |
       | priority   | None                                 |
       | ttl        | None                                 |
       | type       | A                                    |
       | domain_id  | 1fb5d17c-efaf-4e3c-aac0-482875d24b3e |
       +------------+--------------------------------------+

