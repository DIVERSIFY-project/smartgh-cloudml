from plumbum import local
from monkeylib import add_to_container_meta, container_meta
docker = local["docker"]

for i in docker["ps"]["-a", "-q"]().split():
    add_to_container_meta(i)

print container_meta
