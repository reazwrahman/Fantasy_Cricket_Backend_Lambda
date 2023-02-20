# Fantasy_Cricket_Backend_Lambda
Fantasy_Cricket_Backend_Lambda 

useful instructions for future: 
mac os x has library incompatibilities with lambda's linux x86-64 architecture 
always use zappa to create the base package, zappa uses local cache to download 
packages that uses manylinux64 wheel. 
Follow the zappa_setting.json file in this repo.  

1) running `zappa init` will create a base zappa_setting.json[one time effort for new repo] 
2) add the production key - no need to have any content. follow the template in this repo [one time effort for new repo] 

how to update lambda in the aws: 
1) enable prod_venv venv (source prod_venv/bin/activate) 
note: it's idential to local, except the pandas and numpy library 
2) pip install -r prod_requirements.txt 
3) run `zappa package production -o backend_lambda.zip` 
this will create a zip file with linux based wheels 
4) now add your code to that zip by runninng `zip -r backend_lambda.zip .` 
5) upload zip with aws console

that's all. eNJOY
