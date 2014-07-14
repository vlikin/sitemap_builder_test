The test task to get a job as a python developer :)

This is a script that builds a sitemap of a site with a defined depth.

Use to save results to the file.
> python ./sitemap.py --depth=4 --output-csv=output.csv http://shelepen.com.ua

Use to output results on the screen.
> python ./sitemap.py --depth=4 http://shelepen.com.ua

There are two classes Sitemap, Page.
Sitemap processes and controls the parsing process. The Page object keeps object information and represents it.

To run tests use this:
> python -m unittest -v test.sitemap