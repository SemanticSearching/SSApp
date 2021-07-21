<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[comment]: <> ([![Contributors][contributors-shield]][contributors-url])

[comment]: <> ([![Forks][forks-shield]][forks-url])

[comment]: <> ([![Stargazers][stars-shield]][stars-url])

[comment]: <> ([![Issues][issues-shield]][issues-url])

[comment]: <> ([![MIT License][license-shield]][license-url])

[comment]: <> ([![LinkedIn][linkedin-shield]][linkedin-url])



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/SemanticSearching/SSApp">
    <img src="./images/logo.png" alt="Logo" width="42.4" height="35.6">
  </a>

<h3 align="center">Semantic Segment Search</h3>

[comment]: <> (  <p align="center">)

[comment]: <> (    An awesome README template to jumpstart your projects!)

[comment]: <> (    <br />)

[comment]: <> (    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>)

[comment]: <> (    <br />)

[comment]: <> (    <br />)

[comment]: <> (    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>)

[comment]: <> (    ·)

[comment]: <> (    <a href="https://github.com/othneildrew/Best-README-Template/issues">Report Bug</a>)

[comment]: <> (    ·)

[comment]: <> (    <a href="https://github.com/othneildrew/Best-README-Template/issues">Request Feature</a>)

[comment]: <> (  </p>)
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#usage">Usage</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>

[comment]: <> (    <li><a href="#usage">Usage</a></li>)

[comment]: <> (    <li><a href="#roadmap">Roadmap</a></li>)

[comment]: <> (    <li><a href="#contributing">Contributing</a></li>)

[comment]: <> (    <li><a href="#license">License</a></li>)

[comment]: <> (    <li><a href="#contact">Contact</a></li>)

[comment]: <> (    <li><a href="#acknowledgements">Acknowledgements</a></li>)
  </ol>
</details>



<!-- ABOUT THE PROJECT -->

## About The Project

[![Product Name Screen Shot][product-screenshot]](https://semanticsearch.site/)

Semantic Segment Search (SSS) is a searching engine which empowers the 
users to search the semantic related results on segment level.
### Usage
* When you first time run this web app, it will find if 
  `/app/db_storage/faiss_index.pickle` exists. If this file is not existing,
  the app will parse the files in `/app/static/docxs`. You can't login the 
  app until all the files in `/app/static/docxs` are parsed. The fist time 
  paring will be time-consuming if you have many files stored in `/app/static/docxs`.
  
* The only way to add file dynamically after you login the app 
  successfully is to upload the file through the 
  `drop zone` field. If you have many files to be parsed, I recommend you 
  use `scp` command to upload all your files to `/app/static/docxs` and 
  then build the `Dockerfile` again.
  
* Currently, this app only support `.docx` file.
### Built With

* [pySBD](https://github.com/nipunsadvilkar/pySBD)
  
  **pySBD** is a sentence boundary disambiguate api which supports 22 languages. In the original [paper](chrome-extension://oemmndcbldboiebfnladdacbdfmadadm/https://www.aclweb.org/anthology/2020.nlposs-1.15.pdf),
they use [Golden Rules](https://s3.amazonaws.com/tm-town-nlp-resources/golden_rules.txt) to measure the performance of their SBD.
* [mammoth](https://pypi.org/project/mammoth/)
  
  **mammoth** is an api to parser .docx files. It can be also used to convert .docx file to htmls.
In */parser_examples/parser.py*, I list some examples to extract the paragraphs and headings.
  
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
  
  **Flask** is a micro web framework.

* [SQLite](https://www.sqlite.org/index.html)

  **SQLite** is a relationl database management system.

<!-- GETTING STARTED -->

## Deploy the APP on Apache2

### Prerequisites

* Anaconda
  ```angular2html
  wget https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh
  bash Anaconda3-2021.05-Linux-x86_64.sh
  ```
* Apache2
  ```angular2html
  sudo apt update
  sudo apt install apache2
  ```
* WSGI
  ```angular2html
  sudo apt update
  sudo apt-get install libapache2-mod-wsgi-py3
  ```

### Installation

* Set Up Conda Env
  ```angular2html
  git clone https://github.com/SemanticSearching/SSApp.git
  cd SSApp
  conda env create -f py38.pml
  conda activate py38
  cd /app/parser_engine/pySBD
  pip install -e ./
  ```
* Set Up the Soft Link 
  ```angular2html
  sudo ln -sT /project/path/of/SSApp /var/www/html/SSApp
  ```
* Set Env Variable in py38
  ```angular2html
  conda activate py38
  conda env config vars set DOMAIN="your domain name begins with http:// or 
  https://"
  conda env config vars set USERNAME="your user name, default is parc"
  conda env config vars set PASSWORD="your password, default is sss"
  ```
* Configure Apache2
  * Enable SSL
    ```angular2html
    sudo a2enmod ssl
    ```
  * Edit "/etc/apache2/site-enables/000-default.conf"
    ```angular2html
    <VirtualHost *:443>
        # The ServerName directive sets the request scheme, hostname and port that
        # the server uses to identify itself. This is used when creating
        # redirection URLs. In the context of virtual hosts, the ServerName
        # specifies what hostname must appear in the request's Host: header to
        # match this virtual host. For the default virtual host (this file) this
        # value is not decisive as it is used as a last resort host regardless.
        # However, you must set it for any further virtual host explicitly.
        #ServerName www.example.com

        ServerAdmin webmaster@localhost
        ServerName your-domain-name
        ServerAlias your-domain-name
        DocumentRoot /var/www/html
        SSLEngine on
        SSLCertificateFile /your/path/of/site_public.crt
        SSLCertificateKeyFile /your/path/of/site.key
        SSLCertificateChainFile /your/path/of/site_chain.crt

        WSGIDaemonProcess SSApp python-path=/your/path/of/py38/lib/python3.8/site-packages
        WSGIScriptAlias / /var/www/html/SSApp/ssapp.wsgi
        WSGIProcessGroup SSApp
        WSGIApplicationGroup %{GLOBAL}
        <Directory /var/www/html/SSApp>
                #WSGIProcessGroup SSApp
                #WSGIApplicationGroup %{GLOBAL}
                Order allow,deny
                Allow from all
        </Directory>


        # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
        # error, crit, alert, emerg.
        # It is also possible to configure the loglevel for particular
        # modules, e.g.
        #LogLevel info ssl:warn

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        # For most configuration files from conf-available/, which are
        # enabled or disabled at a global level, it is possible to
        # include a line for only one particular virtual host. For example the
        # following line enables the CGI configuration for this host only
        # after it has been globally disabled with "a2disconf".
        #Include conf-available/serve-cgi-bin.conf
    </VirtualHost>
    ```
    
* ssapp.wsgi
  
  ```angular2html
  import sys
  sys.path.insert(0, '/var/www/html/SSApp')
  from ssapp import app as application
  ```
  
* Create a Group
  ```angular2html
  # create a group named ssapp
  sudo groupadd ssapp
  # add user www-data 
  sudo adduser www-data ssapp
  # add the ec2 user name to ssapp, the default is ubuntu.
  sudo adduser your-ec2-user-name ssapp
  ```

* Change the Permission of the Folder
  
  Flask, the default user name of which is www-data, will access to the 
  database or static files at running time, so, we need to assign read and 
  write permissions to www-data which belongs to ssapp group.
  ```angular2html
  sudo chown -vR :ssapp /your/path/of/SSApp/
  sudo chmod -vR g+w /your/path/of/SSApp/
  sudo service apache2 restart
  ```

# Deploy the app on Docker Containers
## Args in Docker
```angular2html
# Database
DB_USER: aws postgresql database user
DB_PASS: aws postgresql database password
DB_HOST: aws postgresql database host
DB_NAME: aws postgresql database name
# UI
LOGIN_USER: login user
LOGIN_PASSWORD: login password
# 
APP_ADDR: domain of app, without http://, like semanticsearch.site
```
## Build the Images
# Run Spring-boot-admin
```angular2html
docker run --rm -p 8080:8080 michayaak/spring-boot-admin:2.2.3-1
```
# Run SSApp
Use the following two commands to build the image and run the container.
```angular2html
sudo docker build -t ssapp:latest --build-arg DB_USER=xx --build-arg 
DB_PASS=xx --build-arg DB_HOST=xx --build-arg DB_NAME=xx --build-arg 
LOGIN_USER=xx --build-arg LOGIN_PASSWORD=xx --build-arg APP_ADDR=xx .

sudo sudo docker run --name ssapp -d -p 8000:5000 --rm ssapp:latest
```

<!-- USAGE EXAMPLES -->

[comment]: <> (## Usage)

[comment]: <> (Use this space to show useful examples of how a project can be used. Additional)

[comment]: <> (screenshots, code examples and demos work well in this space. You may also link)

[comment]: <> (to more resources.)

[comment]: <> (_For more examples, please refer to the [Documentation]&#40;https://example.com&#41;_)



<!-- ROADMAP -->

[comment]: <> (## Roadmap)


<!-- CONTRIBUTING -->

[comment]: <> (## Contributing)

[comment]: <> (Contributions are what make the open source community such an amazing place to)

[comment]: <> (be learn, inspire, and create. Any contributions you make are **greatly)

[comment]: <> (appreciated**.)

[comment]: <> (1. Fork the Project)

[comment]: <> (2. Create your Feature Branch &#40;`git checkout -b feature/AmazingFeature`&#41;)

[comment]: <> (3. Commit your Changes &#40;`git commit -m 'Add some AmazingFeature'`&#41;)

[comment]: <> (4. Push to the Branch &#40;`git push origin feature/AmazingFeature`&#41;)

[comment]: <> (5. Open a Pull Request)

<!-- LICENSE -->

[comment]: <> (## License)

[comment]: <> (Distributed under the MIT License. See `LICENSE` for more information.)



<!-- CONTACT -->

[comment]: <> (## Contact)

[comment]: <> (Your Name - [@your_twitter]&#40;https://twitter.com/your_username&#41; -)

[comment]: <> (email@example.com)

[comment]: <> (Project)

[comment]: <> (Link: [https://github.com/your_username/repo_name]&#40;https://github.com/your_username/repo_name&#41;)



<!-- ACKNOWLEDGEMENTS -->

[comment]: <> (## Acknowledgements)

[comment]: <> (* [GitHub Emoji Cheat Sheet]&#40;https://www.webpagefx.com/tools/emoji-cheat-sheet&#41;)

[comment]: <> (* [Img Shields]&#40;https://shields.io&#41;)

[comment]: <> (* [Choose an Open Source License]&#40;https://choosealicense.com&#41;)

[comment]: <> (* [GitHub Pages]&#40;https://pages.github.com&#41;)

[comment]: <> (* [Animate.css]&#40;https://daneden.github.io/animate.css&#41;)

[comment]: <> (* [Loaders.css]&#40;https://connoratherton.com/loaders&#41;)

[comment]: <> (* [Slick Carousel]&#40;https://kenwheeler.github.io/slick&#41;)

[comment]: <> (* [Smooth Scroll]&#40;https://github.com/cferdinandi/smooth-scroll&#41;)

[comment]: <> (* [Sticky Kit]&#40;http://leafo.net/sticky-kit&#41;)

[comment]: <> (* [JVectorMap]&#40;http://jvectormap.com&#41;)

[comment]: <> (* [Font Awesome]&#40;https://fontawesome.com&#41;)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge

[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge

[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members

[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge

[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers

[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge

[issues-url]: https://github.com/othneildrew/Best-README-Template/issues

[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge

[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555

[linkedin-url]: https://linkedin.com/in/othneildrew

[product-screenshot]: images/screenshot.png
