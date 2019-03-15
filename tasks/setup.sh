if [ ! -z $1 ]
then
    APP_ENGINE_SDK=${1%/}
    CURRENT_PATH=`pwd`
    # Create Lib directory if doesn't exist.
    if [ -d "${CURRENT_PATH}/lib" ]
    then
        logger -s -t [INFO] "remove ${CURRENT_PATH}/lib"
        rm -rf "${CURRENT_PATH}/lib"
    fi
    logger -s -t [INFO] "create ${CURRENT_PATH}/lib"
    mkdir "${CURRENT_PATH}/lib"
    if [ -d "${CURRENT_PATH}/venv" ]
    then
        logger -s -t [INFO] "remove ${CURRENT_PATH}/venv"
        rm -rf "${CURRENT_PATH}/venv"
    fi
    logger -s -t [INFO] "create virtual env on ${CURRENT_PATH}/venv"
    # Install venv.
    virtualenv -q -p python2.7 ${CURRENT_PATH}/venv || logger -s -t [ERROR] "Failed to create virtualenv."

    # Pip install in venv.
    dev_file="${CURRENT_PATH}/requirements.txt"
    logger -s -t [INFO] "upgrade pip"
    ${CURRENT_PATH}/venv/bin/pip2 install --upgrade -q pip setuptools
    logger -s -t [INFO] "install ${dev_file}"
    ${CURRENT_PATH}/venv/bin/pip2 install -q -r ${dev_file} -t lib || logger -s -t [ERROR] "failed install ${dev_file}"
    logger -s -t [INFO] "Patching Google App Engine dependencies"
    # Patching Google App Engine dependencies
    PATHS="${CURRENT_PATH}/lib/
    ${APP_ENGINE_SDK}
    ${APP_ENGINE_SDK}/lib/
    importsite;site.addsitedir(u'lib')"
    echo "${PATHS}" > "${CURRENT_PATH}/venv/lib/python2.7/site-packages/lib.pth"


    echo "Setup script ended successfully"
else
    echo "No google_sdk Path. Please provide one. Example : $0 /usr/lib/google-cloud-sdk/platform/google_appengine"
fi
