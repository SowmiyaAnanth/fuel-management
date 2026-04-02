from db import owner_collection
from bson import ObjectId
from bson.errors import InvalidId

class OwnerService:

    def _format_owner(self, owner):
        if not owner:
            return None
        return {
            "owner_id": str(owner["_id"]),
            "full_name": owner.get("full_name"),
            "nic": owner.get("nic"),
            "mobile_no": owner.get("mobile_no"),
            "email": owner.get("email"),
            "address": owner.get("address"),
            "district": owner.get("district"),
        }
    
    def _is_valid_object_id(self, owner_id: str):
        try:
            ObjectId(owner_id)
            return True
        except InvalidId:
            return False
        
    def get_all(self):
        owners = owner_collection.find()
        return [self._format_owner(owner) for owner in owners]
    
    def get_by_id(self, owner_id: str):
        if not self._is_valid_object_id(owner_id):
            return None
        
        owner = owner_collection.find_one({"_id": ObjectId(owner_id)})
        return self._format_owner(owner)
    
    def create(self, owner_data):
        owner_dict = owner_data.model_dump()

        existing_owner = owner_collection.find_one({"nic": owner_dict["nic"]})
        if existing_owner:
            return None
        
        result = owner_collection.insert_one(owner_dict)
        created_owner = owner_collection.find_one({"_id": result.inserted_id})
        return self._format_owner(created_owner)
    
    def update(self, owner_id: str, owner_data):
        if not self._is_valid_object_id(owner_id):
            return None
        
        update_data = owner_data.model_dump(exclude_unset=True)
        if not update_data:
            return "NO_FIELDS"
        
        if "nic" in update_data:
            existing_owner = owner_collection.find_one({
                "nic": update_data["nic"],
                "_id": {"$ne": ObjectId(owner_id)}
            })
            if existing_owner:
                return "NIC_EXISTS"
            
        result = owner_collection.update_one(
            {"_id": ObjectId(owner_id)},
            {"$set": update_data}
        )

        if result.matched_count > 0:
            updated_owner = owner_collection.find_one({"_id": ObjectId(owner_id)})
            return self._format_owner(updated_owner)
        
        return None
    
    def delete(self, owner_id: str):
        if not self._is_valid_object_id(owner_id):
            return False
        
        result = owner_collection.delete_one({"_id": ObjectId(owner_id)})
        return result.deleted_count > 0