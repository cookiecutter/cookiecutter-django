#!/bin/bash


# NAME parameter of each environment is used to define 
# settings module, virtualenv name and requirements file.

# To setup virtualenvs 
# 1. Create the requirements file  in requirements folder. 
# 2. Create an evironment settings section in this file 
# 3. Run this script from parent folder 
#    ./scripts/setup_env.sh 


# This script creates virtual environments and adds DB,
# settings module and  secret key in virtualenv activation hooks
# This script does not check for existing virtualenv  



# Settings 
PIP='pip' 
DJ_SETTINGS='config.settings.'
PROJ_NAME='project_name'   #<---- Change This 

# Secret Key Generator ( No special chrs ; not so secure ) 
KEYGEN=`python2.7 -c 'import random; import string; print "".join([random.SystemRandom().choice(string.digits + string.letters ) for i in range(100)])'`
SK='KEYGEN'

# Environments and Parameters  #<---- Change This  ( Add sections )
declare -A PRODUCTION   
PRODUCTION['NAME']='production'
PRODUCTION['DB_URL']='postgres://lab:lab@127.0.0.1:5432/'${PROJ_NAME}'_production'
eval PRODUCTION['SKEY']=\$${SK}

declare -A LOCAL
LOCAL['NAME']='local'
LOCAL['DB_URL']='postgres://lab:lab@127.0.0.1:5432/'${PROJ_NAME}'_local'
eval LOCAL['SKEY']=\$${SK}

declare -A TEST
TESTL['NAME']='test'
TEST['DB_URL']='postgres://lab:lab@127.0.0.1:5432/'${PROJ_NAME}'_test'
eval TEST['SKEY']=\$${SK}

APP_VENVS=( 'LOCAL' 'PRODUCTION' 'TEST' )  #<------ Change This 


# Settings VARs stay above this comment 
# Source virtualenvwrapper for command mkvirtualenv and friends

VENV_SH=`env | grep virtualenvwrapper.sh  | awk -F= '{print $2}'`
if [ -z ${VENV_SH} ];then
   echo 'Unable to source virtualenvwrapper.sh'
   exit 1
fi
source ${VENV_SH}


echo 'WORKON_HOME is  '${WORKON_HOME}

# Iterate over the VENV Definitions 
# Create Virtual Env and place ENV vars in hook files
for venv in "${APP_VENVS[@]}" 
do
  eval DB_URL=\${${venv}['DB_URL']}
  eval NAME=\${${venv}['NAME']}
  eval SKEY=\${${venv}['SKEY']}

  mkvirtualenv ${PROJ_NAME}_${NAME} 
  workon ${PROJ_NAME}_${NAME}
  ${PIP} install -r requirements/${NAME}.txt
  
  cat << EOF > ${WORKON_HOME}/${PROJ_NAME}_${NAME}/bin/postactivate 
export DJANGO_SETTINGS_MODULE=${DJ_SETTINGS}${NAME}
export DATABASE_URL='${DB_URL}'
export SECRET_KEY='${SKEY}'
EOF

  cat << EOF > ${WORKON_HOME}/${PROJ_NAME}_${NAME}/bin/predeactivate 
unset DJANGO_SETTINGS_MODULE
unset SECRET_KEY
unset DATABASE_URL
EOF

done 



