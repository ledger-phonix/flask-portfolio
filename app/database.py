from pymongo import MongoClient 
from datetime import datetime
import pytz
from bson import ObjectId
Pk_TZ = pytz.timezone('Asia/Karachi')

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.testimonials = None
        self.subscribers = None
        self.projects = None
        self.certificates = None
        self.counters = None
    def connect(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.projects = self.db['projects']
        self.certificates = self.db['certificates']
        self.testimonials = self.db['testimonials']
        self.subscribers = self.db['subscribers']
        self.counters = self.db['counters']
        
        #for testimonials
        if self.counters.find_one({"_id": "testimonial_id"}) is None:
            self.counters.insert_one({"_id" : "testimonial_id" , "seq": 0})
        #for subscribers
        if self.counters.find_one({"_id" : "subscriber_id"})   is None:
            self.counters.insert_one({"_id" : "subscriber_id", "seq" : 0}) 
        # for projects
        if self.counters.find_one({"_id" : "project_id"}) is None:
            self.counters.insert_one({"_id" : "project_id", "seq": 0})
         # for certificates
        if self.counters.find_one({"_id" : "certificate_id"}) is None:
            self.counters.insert_one({"_id" : "certificate_id", "seq": 0})
            
    def get_next_id(self, counter_name):
        #increment the counter and return the new number(1,2,3......)
       
        counter = self.counters.find_one_and_update(
            {"_id" : counter_name},
            {"$inc": {"seq" : 1}},
            return_document= True
        )
        return counter["seq"]
       
        
    def save_testimonials(self, data):
        now_in_pk = datetime.now(Pk_TZ)
        data['created_at_human'] = now_in_pk.strftime("%d-%m-%Y %I:%M %p")
        # Add ID and PK time then save to mongoDB
        data["t_id"] = self.get_next_id("testimonial_id")
        data['created_at'] = now_in_pk
        
        return self.testimonials.insert_one(data)
    
    def save_email(self, email):
        data = {
            "s_id" : self.get_next_id("subscriber_id"),
            "email" : email,
            "created_at" : datetime.now(Pk_TZ)
        }
        return self.subscribers.insert_one(data)
    def save_projects(self, data):
        now_in_pk = datetime.now(Pk_TZ)
        data['created_at_human'] = now_in_pk.strftime("%d-%m-%Y %I:%M %p")
        # Add ID and PK time then save to mongoDB
        data["p_id"] = self.get_next_id("project_id")
        data['created_at'] = now_in_pk
        
        return self.projects.insert_one(data)
    def save_certificates(self, data):
        now_in_pk = datetime.now(Pk_TZ)
        data['created_at_human'] = now_in_pk.strftime("%d-%m-%Y %I:%M %p")
        # Add ID and PK time then save to mongoDB
        data["p_id"] = self.get_next_id("project_id")
        data['created_at'] = now_in_pk
        
        return self.certificates.insert_one(data)
    
    def get_all_projects(self):
        projects = self.db.projects.find().sort("created_at", -1)
        return list(projects)
    
    def get_all_certificates(self):
        certificates = self.db.certificates.find().sort("created_at", -1)
        return list(certificates)
    
    def get_all_testimonials(self):
        testimonials = self.db.testimonials.find().sort('created_at' , -1) 
        return list(testimonials)
    def update_testimonial_status(self, t_id, status):
        return self.db.testimonials.update_one(
        {'_id': ObjectId(t_id)}, 
        {'$set': {'t_display': status}}
    )
    def get_active_testimonials(self):
        testimonials = self.db.testimonials.find({'t_display': True}).sort('created_at', -1)
        return list(testimonials)
db_handler = Database()