# Autocomic
This is a script that turns online comics into pdf's. Given a 'comic.json' or 'comic.yml' file with certain attriubyes, it can crawl and convert any newly any webcomic.

## Installation
Installation for this script is a pain. Internally, autocomic runs a python script which generates a 
LaTeX file which it compiles into a pdf. This has many efficiency and layout benefits (for example, 
if you modify the comic.json file and re-run the script, it can change the formatting of the pdf 
without having to re-download every comic). Unfortunately, this makes it pretty hard to install. 
You will need:

Python 3
 - requests
 - lxml
 - urllib
 - matplotlib
 - numpy
 - PIL

[Rubber (LaTeX compiler)](https://github.com/petrhosek/rubber)
 - graphicx
 - xcolor
 - pagecolor
 - fancyhdr
 - sectsty
 - tocloft

## Usage
Once you have all of the above working, you can generate a directory for a new comic with the command
        `generateComic comicName`
where comicName is the name of the directory that will be generated. Once the directory is generated, 
change it to the active directory (
      `cd comicName`
) and edit the 'comic.yml' file with the editor of your choice (see details below). Once the file is
edited, run 
       `comic`
and the generation can begin. At any time, you can stop the process with SIGINT (^C on linux) and the script
will clean up after itself. Running
       `comic`
in that directory at any time will resume where the script left off, including if the script terminated
because it reached the last comic.

### comic.yml
comic.yml contains the following variables:
 - name: name of the comic; will be on the first page of the pdf.
 - author: author of the comic; will be on the first page of the pdf. Optional.
 - pageColor: an array of rgb values of the color that the page will be (from 0-255)
 - textColor: color for titles and mouseover text
 - comicSelect: a valid css selector to grab the img tag of the comic (e.g. "#comic img")
 - titleSelect: a valid css selector for the title of the comic. If left empty, script will assume
that each strip/page does not have a title
 - mouseover: true will take the title text of each strip/page and write it beneath the comic.
 - nextSelect: a valid css selector for the link to the next comic (e.g. "a[rel='next']")
 - firstURL: the URL of the first page/strip
 - chapters: if set to true, generated pdf will have chapters. If set, also use the chapterElement and chapterRegex attributes
 - chapterElement: [optional] a valid css selector for the HTML element containing the chapter name. 
Used only if chapters is set to true
 - chapterRegex: [optional] a regex selecting the chapter name from the text of the element. If you want the entire
text, use ".\*".
 - optionalHeight: [optional] some comics need a different page height. specify this as a value in pixels and the pages pf the generated pdf will be that height.
 - useCSS: [optional] defaults to true. If set to false, comicSelect, nextSelect, and chapterElement will expect a regex for selecting the correct element rather than the CSS selectors. In general, this is hard to use and inconsistent. It may be necessary for some comics with inconsistent page design between strips, but should only be used as a last resort. (Out of the hundreds of comics tried, this option was needed for only one comic).

### cleanup
Running 
       `cleanupComic`
will delete all files generated by the script, leaving only the comic.json file. Useful if the images and
LaTeX files are not needed anymore or if something goes wrong.
