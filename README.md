# Wikipedia Social Research

## Info

## Guidance

### Step 1
Clone the project to a folder

### Step 2
After cloning the project you should have a following folder structure:

-----------------------------------------------------------------------
```
wikipedia-social-research-private/
├── collect_data_eric/
│   ├── main.py
│   ├── utils.py
│   └── config/
│       ├── settings.yaml
│       └── defaults.yaml
├── FetchingRelevantPoliticians/
│   ├── test_main.py
│   └── test_utils.py
├── Merging_Plotting/
│   ├── test_main.py
│   └── test_utils.py
├── ProjectAITestData/
│   ├── .DS_Store
│   ├── MoreComplex/
│   │   ├── Revisions_Timeline_Comp.py
│   │   └── Wikipedia_Revisions_Pipeline.py
│   └── SimpleAnalysis/
│       ├── import_requests.py
│       ├── Revisions_Timeline_Comp.py
│       ├── Revisions_Timeline_Simple.py
│       └── Wikipedia_Revisions_Pipeline.py
└── README.md
```

### Step 3
Replicate the fetching and analysis of the research. To do that you can first try to get an understanding of what will be done using the test data like we did. As you can see there is a folder called ProjectAITestData. Inside of that folder there are two more folders MoreComplex and SimpleAnalysis. That is the place where you can try to do a bit of testing of fetching data from wikipedia and analysing it. *This step can be done but is not necessary and does not have any link with the actual real research that was one.*

#### Step 3.1 Test data (optional)
First we need to make sure to run all of the scripts in the correct folder. Since we will start with SimpleAnalysis we need to make sure that the path where we execute the scripts is *~\wikipedia-social-research-private\ProjectAITestData\SimpleAnalysis>* and after we make sure we have the right path we can do the following:
  - execute import_requests.py
  - a file will get generated *~\wikipedia-social-research-private\ProjectAITestData\SimpleAnalysis\Alexander_Thumfart_revisions.csv_revisions.csv* where all of the revisions from the given politician will be fetched from wikipedia and saved in this csv file, after that we can look at the file to see and analyse what we created
  - after that we execute *Wikipedia_Revisions_Pipeline.py* and 5 new folders named after countries get generated in SimpleAnalysis folder with corresponding csv files of politicians
  - since we now have a bit more data we can now execute *Revisions_Timeline_Simple.py* and it will create histograms in each folder of each country as png that is called *{country}_revisions_histogram.png* and we can take a look at each of them
  - now we can also execute *Revisions_Timeline_Comp.py* and ti will also create png files in each folder of each country called *{country}_revision_trends.png* which presents a timeline of all revisions of politicians of that country

Now, we can also do more complex fetching and analysis of wikipedia articles. We need to go over to the path *~\wikipedia-social-research-private\ProjectAITestData\MoreComplex>* and then:
  - execute *Wikipedia_Revisions_Pipeline.py* and 7 new folders named after countries get generated in MoreComplex folder with corresponding csv files of politicians
  - now we can execute the script called *Revisions_Timeline_Comp.py* and a png file with the timeline named *{country}_revision_trends.png* will get generated in every countrys' folder





