## Additional installation steps (tested on ubuntu 22.04LT)to install and modify ImageMagick

1. Locate policy.xml and modify if you are getting errors white using the TextClip class of moviepy.
To locate the file
```
locate policy.xml
```

Modify  /etc/ImageMagick-6/policy.xml by first checking if following line -
`<policy domain="path" rights="none" pattern="@*" />` is commented.  If not, please comment it.


2. Find the package name which uses this particular policy- 
```
dpkg -S /etc/ImageMagick-6/policy.xml 
```

3. Note down the name of package (on Ubuntu 22.04 LTS, it is likely to be `imagemagick-6-common`)

4. Reload package so that the changes in policy.xml would take effect.

```
sudo dpkg-reconfigure imagemagick-6-common
```