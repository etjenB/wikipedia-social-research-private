# Wikipedia Social Research

### Step 1
Clone the project to a folder

### Step 2
After cloning the project you should have a following folder structure:

-----------------------------------------------------------------------
```
wikipedia-social-research-private/
├── FetchingRelevantPoliticians/
│   ├── Revisions/
│   │   ├── merge_revisions_uk.py
│   │   └── merge_revisions_usa.py
│   ├── UK/
│   │   ├── house_of_commons_2010.py
│   │   ├── house_of_commons_2015.py
│   │   ├── house_of_commons_2017.py
│   │   ├── house_of_commons_2019.py
│   │   └── house_of_commons_2024.py
│   └── USA/
│       ├── HouseOfRepresentatives/
│       │   ├── 113th_congress_hor.py
│       │   ├── 114th_to_116th_congress_hor.py
│       │   ├── 117th_congress_hor.py
│       │   └── 118th_congress_hor.py
│       └── Senate/
│           ├── 113th_congress.py
│           └── 114th_to_118_congress.py
├── FetchingRelevantPoliticiansGerAu/
│   ├── collect_data.py
│   └── wiki_links.py
├── Merging_Plotting/
│   ├── Create_AUS_GER_CSVs.py
│   ├── Create_UK_US_CSVs.py
│   ├── Mapping_Parties.py
│   └── Plotting_Revisions.py
├── ProjectAITestData/
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

#### Step 3.2 Fetching politicians
All of the scripts need to be ran in the correct folder. Fetching of the UK politicians is done in FetchingRelevantPoliticians\UK so now our path needs to be *~\wikipedia-social-research-private\FetchingRelevantPoliticians\UK>* and now that we are at the right path we:
  - execute scripts *house_of_commons_2010.py*, *house_of_commons_2015.py*, *house_of_commons_2017.py*, *house_of_commons_2019.py*, *house_of_commons_2024.py*
  - folder called election_data will be generated with csv files for all elections from 2010 to 2024, so 5 csv files

After this we can go to USA folder, so our path is *~\wikipedia-social-research-private\FetchingRelevantPoliticians\USA>* and there we have two folders for House of Representatives and Senate. In there we have scripts but we all of the scripts need to be executed in the USA path so we don't change the path *~\wikipedia-social-research-private\FetchingRelevantPoliticians\USA>* and there we can:
  - execute scripts from the HouseOfRepresentatives folder *113th_congress_hor.py*, *114th_to_116th_congress_hor.py*, *117th_congress_hor.py*, *118th_congress_hor.py*
  - folder called *representatives_data* will be generated and inside it 6 csv files for each elections from 113th to 118th
  - execute the two scripts from the Senate folder *113th_congress.py* and *114th_to_118_congress.py*
  - new folder called *senators_data* will be generated and inside it 6 csv files for each elections from 113th to 118th

Next we have to execute merge scripts that are located in Revisions Folder inside FetchingRelevantPoliticians folder. So, what we need to do is we stay in the USA path *~\wikipedia-social-research-private\FetchingRelevantPoliticians\USA>* and there we:
  - execute the *merge_revisions_usa.py*
  - a folder called *USA_politicians* will be generated containing csv files for all of politicians individually with their revisions from their wikipedia pages

Now, we have to go to UK path, so our path should be *~\wikipedia-social-research-private\FetchingRelevantPoliticians\UK>* and then:
  - execute script *merge_revisions_uk.py*
  - a new folder called *UK_Politicians* gets created with csv files of revisions for each UK politicians' wikipedia page

Fetching of the German and Austrian politicians is done in FetchingRelevantPoliticiansGerAu so now our path needs to be *~\wikipedia-social-research-private\FetchingRelevantPoliticiansGerAu>* and now that we are at the right path we:
  - run the script *wiki_links.py*
  - a new folder called *Germany_Austria_data* is generated with csvs from German and Austrian elections
  - run the script *collect_data.py*
  - a new folder *Revisions* gets generated containing csv files for all of politicians individually with their revisions from their wikipedia pages 

#### Step 3.3 Data analysis
For the data analysis we need to go to the Merging_Plotting folder so our path should be *~\wikipedia-social-research-private\Merging_Plotting>* and after that:
  - we run the script *Create_UK_US_CSVs.py*
  - *RevisionData* folder gets generated with csv files for uk and us
  - we run the script *Create_AUS_GER_CSVs.py*
  - in the folder *RevisionData* additional csv files for germany and austria get generated

Now that our data is ready we can do the mapping of the parties by running script *Mapping_Parties.py* and as a final step we can plot the data in any appropriate way using script *Plotting_Revisions.py*.


