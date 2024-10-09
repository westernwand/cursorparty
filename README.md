# cursorparty
## description:
cursorparty is a containerized novelty created for the purpose of encouraging cursor socialization.
## why?
why not?
## getting started guide:
1. build it:
```
docker build --tag cursorparty-frontend --file .\cursorparty-frontend.dockerfile .
docker run -it --rm -d -p 8080:80 cursorparty-frontend
```
2. [localhost:8080](http://localhost:8080/)

## todo:
 - [x] spin up nginx container
 - [ ] simple frontend with nginx
 - [ ] router with python
 - [ ] swarm router containers
 - [ ] swarm frontend containers
 - [ ] load balance between router containers