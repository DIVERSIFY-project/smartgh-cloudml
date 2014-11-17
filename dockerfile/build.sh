cd base
docker build -t songhui/smhp-base .

cd ../sensor
docker build -t songhui/smhp-sensor .

cd ../hopper
docker build -t songhui/smhp-hopper .
