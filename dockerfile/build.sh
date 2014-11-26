cd base
docker build --no-cache=false -t songhui/smhp-base .

cd ../sensor
docker build --no-cache=false -t songhui/smhp-sensor .

#cd ../hopper
#docker build -t songhui/smhp-hopper-fast .

cd ../web
docker build --no-cache=true -t songhui/smhp-web .

cd ../hopper
docker build --no-cache=true -t songhui/smhp-hopper .

