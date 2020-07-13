import pymongo
from bson.objectid import ObjectId



class ManageLKB(object):
    def __init__(self, host):

        self.host = host
        self.client = pymongo.MongoClient(self.host)


    def insert_clause_db(self, cls):

        db = self.client["ad-caspar"]
        clauses = db["clauses"]

        features = self.extract_features(cls)
        print("\nfeatures:", features)

        try:

            clause = {
                "value": cls,
                "features": features
                }
            sentence_id = clauses.insert_one(clause).inserted_id
            print("sentence_id: " + str(sentence_id))

        except pymongo.errors.DuplicateKeyError:
             print("\nClause already present in Lower KB!")



    def extract_features(self, sent):
        chunks = sent.split(" ")
        def_chinks = []
        for chu in chunks:
            chinks = chu.split("(")
            for chi in chinks:
                if ')' not in chi and chi not in def_chinks and chi != '' and chi != "==>":
                    def_chinks.append(chi)
        return def_chinks



    def show_LKB(self):

        db = self.client["ad-caspar"]
        clauses = db["clauses"]

        myclauses = clauses.find()
        for cls in myclauses:
            print("\n")
            print(cls['value'])
            print(cls['features'])
        return myclauses.count()


    def clear_lkb(self):

        db = self.client["ad-caspar"]
        clauses = db["clauses"]
        x = clauses.delete_many({})
        return x.deleted_count



    def get_related_clauses(self, cls):

        db = self.client["ad-caspar"]
        features = self.extract_features(cls)
        feat_num = len(features)

        aggr = db.clauses.aggregate([
            {"$project": {
                "value": 1,
                "intersection": {"$size": {"$setIntersection": ["$features", features]}}
            }},
            {"$group":
                 {"_id": "$intersection",
                  "group": {"$push": "$value"}}},
            {"$sort": {"_id": -1}},
            {"$limit": 1}
        ])

        new_clauses = []
        for a in aggr:
            occurrencies = a['_id']
            confidence = int(occurrencies) / int(feat_num)
            print("confidence: ", confidence, "\n")
            new_clauses = a['group']
        return new_clauses





    """
    def get_fol_from_db(self, id): 

        db = self.client["ad-caspar"]
        terms = db["clauses"]
        fol = []

        query = {'sentence_id': ObjectId(str(id))}
        mydoc = terms.find(query)
        for t in mydoc:
            clause = []
            term.append(t['value'])
            term.append(t['features'])
            fol.append(term)
        return fol
    """













