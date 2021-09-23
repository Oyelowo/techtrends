1. Launch the virtual machine
`vagrant up`

2. ssh into the virtual machine
`vagrant ssh`

3. make yourself a super user
`sudo su`

4. create host path for volume(developement, staging and production) in the virtual machine
```
function mkfile() { mkdir -p -- "$1" && touch -- "$1"/"$2";}
mkfile /mnt/data/development database.db
mkfile /mnt/data/staging database.db
mkfile /mnt/data/production database.db
```

5. make the deploy script executable and run the script. This launches argocd resources and kubenet resources for the application
```sh
chmod +x ./argocd/deploy_apps.sh
./argocd/deploy_apps.sh
```

5. check that pods are up and running and wait for this
`kubectl get po -A`

6. Get argocd admin dashboard credentials via the command line
  username: admin
  password:
  You can get argocd password by running:
`kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d`

7. Login and deploy the app in various environments
Open the app at: `https://192.168.50.4:30007/`

development:
`192.168.50.4:30020/`
`192.168.50.4:30021/`

staging
`192.168.50.4:30030/`
`192.168.50.4:30031/`

production:
`192.168.50.4:30040/`
`192.168.50.4:30041/`

aside: 192.168.50.4 is the IP of the virtual machine.(can be seen in Vagrantfile)

