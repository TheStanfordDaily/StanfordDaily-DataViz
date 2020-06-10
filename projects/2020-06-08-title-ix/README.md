# Title IX project

Deployed at .

Embedding:

```
<style>
#main-article-text2 {
margin: 0 !important; width: 100% !important;
}
</style>
<iframe id="tsd-custom-iframe" src="https://thestanforddaily.github.io/StanfordDaily-DataViz/projects/2020-06-08-title-ix/index.html" style="border: 0; width: 100%; min-height: 100vh;"></iframe>
```

## Local setup

```
cd projects/2020-06-08-title-ix/
npm install -g live-server
live-server
```

Go to http://localhost:8080 on your computer.


## Image PDF -> PNG commands

  Setup:
  - Install ghostscript and imagemagick.

  Steps:

```
  mkdir images
  convert -density 100 TitleIX.pdf images/TitleIX.png
  # delete first page
  rm images/TitleIX-0.png
  # append pages to get final image
  convert -append images/TitleIX-1.png images/TitleIX-2.png images/TitleIX-3.png images/TitleIX-4.png images/TitleIX-5.png images/TitleIX-6.png images/TitleIX-7.png images/TitleIX-8.png images/TitleIX-9.png images/TitleIX-10.png images/TitleIX-11.png images/TitleIX-12.png images/TitleIX-13.png images/TitleIX-14.png images/TitleIX-15.png images/TitleIX-16.png images/TitleIX-17.png images/TitleIX-18.png images/TitleIX-19.png images/TitleIX-20.png images/TitleIX-21.png images/TitleIX-22.png images/TitleIX-23.png images/TitleIX-24.png images/TitleIX-25.png images/TitleIX-26.png images/TitleIX-27.png images/TitleIX-28.png images/TitleIX-29.png final.png
```