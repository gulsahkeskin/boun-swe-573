import requests
import json


class WikiData:
    def __init__(self, wikiQid):
        tag = requests.get("https://www.wikidata.org/w/api.php?action=wbgetentities&ids=" +
                           wikiQid +
                           "&languages=en&format=json"
                           )

        tag_dict = tag.json().get('entities').get(wikiQid)
        self.fetch_data = tag_dict

    def get_id(self):
        return self.fetch_data.get('id')

    def get_label(self):
        return self.fetch_data.get('labels').get('en').get('value')

    def get_description(self):
        if self.fetch_data.get('descriptions'):
            return self.fetch_data.get('descriptions').get('en').get('value')
        else:
            return None

    # fetch the part of "also known as" of the query in Wikidata
    def get_details(self):
        alias_list = []
        if self.fetch_data.get('aliases'):
            for alias in self.fetch_data.get('aliases').get('en'):
                alias_list.append(alias.get('value'))

        if self.fetch_data.get('claims'):
            # fetch subclass of the query
            if self.fetch_data.get('claims').get('P279'):
                for subclass in self.fetch_data.get('claims').get('P279'):
                    subclass_id = subclass.get('mainsnak').get('datavalue').get('value').get('id')
                    term = WikiData(subclass_id)
                    alias_list.append(term.get_label())

            # fetch symptoms and signs data
            if self.fetch_data.get('claims').get('P780'):
                for symptom in self.fetch_data.get('claims').get('P780'):
                    symptom_id = symptom.get('mainsnak').get('datavalue').get('value').get('id')
                    term = WikiData(symptom_id)
                    alias_list.append(term.get_label())

            # get the information of "said to be the same as" from Wikidata
            if self.fetch_data.get('claims').get('P460'):
                for synonym in self.fetch_data.get('claims').get('P460'):
                    synonym_id = synonym.get('mainsnak').get('datavalue').get('value').get('id')
                    term = WikiData(synonym_id)
                    alias_list.append(term.get_label())

            # fetch the drugs used for treatment of bipolar disorder
            if self.fetch_data.get('claims').get('P2176'):
                for drug in self.fetch_data.get('claims').get('P2176'):
                    drug_id = drug.get('mainsnak').get('datavalue').get('value').get('id')
                    term = WikiData(drug_id)
                    alias_list.append(term.get_label())

        return ', '.join(alias_list)


# term = WikiData('Q131755')
# print(term.get_id())
# print(term.get_label())
# print(term.get_description())
# print(term.get_details())


# Suggest alternative Wikidata tags to choose
# returns different list of options depending on the query
    def wiki_suggest(query):
        wikidata_list = requests.get('https://www.wikidata.org/w/api.php?action=wbsearchentities&search='
                                     + query
                                     + '&format=json&language=en&type=item&continue=0'
                                     )

        wikiJSON = wikidata_list.json()
        query_results = []
        subjects = wikiJSON.get('search')
        if subjects:
            for subject in subjects:
                q_id = subject.get('id')
                label = subject.get('label')
                description = subject.get('description')
                query_results.append(q_id + ": " + label + " - " + description)

        return query_results

# query = "bipolar disorder"
# print(WikiData.wiki_suggest(query))
