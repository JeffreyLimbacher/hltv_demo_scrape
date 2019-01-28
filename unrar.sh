cd demos
find -regex "./[0-9]+.rar" -print0 | sed "s/.rar//g" | xargs -0 -n1 -P2 -I@ bash -c "unrar e -ad @ && cd @ && find * -type f -exec mv {} ../@_{} \;"
