# This README file describes the technical process behind the paper "How to write a CHI paper (asking for a friend)" submitted at alt.chi (CHI 2024).

## Here we describe how to use the code within this repository as well as providing information about the data used and and data collected

** NOTE: Throughout our process we did not update or train any online model or left data in the cloud for other models to use in the future. 
Extracting the papers was trivial and using available online tools. Our use is purely academic and in research context. 

In this repository we do not include the data used to train the model. However, here we detailed how to get the data from the ACM Digital library. 
We used a google chrome extension called webscraper.io, that allows for exploring a website thorugh its HTML elements and extract in an excel or .csv file the data.

Once you have added the webscraper extension, you can import a sitemap, which should be the following

{"_id":"chi23-final","startUrl":["https://dl.acm.org/doi/proceedings/10.1145/3544548"],"selectors":[{"id":"session-click","parentSelectors":["_root"],"type":"SelectorElementClick","clickActionType":"real","clickElementSelector":".sections a.section__title","clickElementUniquenessType":"uniqueText","clickType":"clickOnce","delay":300,"discardInitialElements":"do-not-discard","multiple":true,"selector":".sections a.section__title"},{"id":"session-name","parentSelectors":["_root"],"type":"SelectorText","selector":".sections a.section__title","multiple":true,"regex":""},{"id":"sessions-and-papers","parentSelectors":["_root"],"type":"SelectorText","selector":".sections .js--open a.section__title, .issue-item__title a","multiple":true,"regex":""},{"id":"article-open","parentSelectors":["_root"],"type":"SelectorLink","selector":".js--open .issue-item__title a","multiple":true,"linkType":"linkFromHref"},{"id":"html-format","parentSelectors":["article-open"],"type":"SelectorLink","selector":"a[title='View HTML Format']","multiple":false,"linkType":"linkFromHref"},{"id":"article-titles","parentSelectors":["html-format"],"type":"SelectorText","selector":"h1","multiple":false,"regex":""},{"id":"article-authors","parentSelectors":["html-format"],"type":"SelectorText","selector":"a[ref]","multiple":true,"regex":""},{"id":"article-fullauthors","parentSelectors":["html-format"],"type":"SelectorText","selector":".authorGroup div","multiple":true,"regex":""},{"id":"article-abstact","parentSelectors":["html-format"],"type":"SelectorText","selector":".abstract small","multiple":false,"regex":""},{"id":"article-headers","parentSelectors":["html-format"],"type":"SelectorText","selector":".body h2","multiple":true,"regex":""},{"id":"article-sections","parentSelectors":["html-format"],"type":"SelectorText","selector":".body > section","multiple":true,"regex":""},{"id":"article-ind-bib","parentSelectors":["html-format"],"type":"SelectorText","selector":".bibUl li","multiple":true,"regex":""},{"id":"article-full-table","parentSelectors":["html-format"],"type":"SelectorText","selector":".table-responsive","multiple":true,"regex":""},{"id":"article-table-caption","parentSelectors":["html-format"],"type":"SelectorText","selector":".table-caption","multiple":true,"regex":""},{"id":"article-table","parentSelectors":["html-format"],"type":"SelectorText","selector":".table","multiple":true,"regex":""},{"id":"article-tables","parentSelectors":["html-format"],"type":"SelectorText","selector":"table.table","multiple":true,"regex":""}]}

Once you import this sitemap, you can head to "https://dl.acm.org/doi/proceedings/10.1145/3544548" and start scraping the content. In the end, this will generate either an excel file or .csv file that extracts most of the information per paper such as:

* authors' names and affiliations
* papers' sessions
* papers' sections
* papers' tables
* papers' references

Once the file is done and downloaded, you can import this project that includes all the code to preprocess the data (into the right format both for data analysis and for the model to train KITSUNE).

1. The python code will first transform the raw data into a compressed_view.
2. Then, using this compressed_view, we process and format the data as expected by the Zephyr 7b-beta model.
3. Once this is done, you can use the final generated .xlsl (excel file) to run the jupyter notebook code.
4. Running the jupyter notebook in google colab will allow you to use the GPU and GPU RAM in the cloud, which might be necessary depending on your setup.
5. Once you run the notebook, the model can be used with the example prompts to generate some interesting but mostly useless output.
