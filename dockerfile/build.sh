cd base
docker build --no-cache=true -t songhui/smhp-base .

cd ../sensor
docker build --no-cache=true -t songhui/smhp-sensor .

#cd ../hopper
#docker build -t songhui/smhp-hopper-fast .

cd ../web
docker build --no-cache=true -t songhui/smhp-web .

cd ../hopper-tomcat
docker build --no-cache=true -t songhui/smhp-hopper-tomcat .

