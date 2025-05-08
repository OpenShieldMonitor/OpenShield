# OpenShield

## Descripción


## BBDD

Vamos a utilizar MongoDB contenorizado mediante Docker.

Levantar MongoDB:
```bash
docker-compose up -d
```

Ver los logs del contenedor:
```bash
docker logs -f mongodb_monitor
```

Abrir shell del contenedor MongoDB:
```bash
docker exec -it mongodb_monitor mongosh -u admin -p admin123
```