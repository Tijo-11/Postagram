"""All the objects sent back as a response in our API will contain the id, created, and updated fields. 
It’ll be repetitive to write these fields all over again on every ModelSerializer, so let’s just create 
an AbstractSerializer class. """


from rest_framework import serializers

class AbstractSerializer(serializers.ModelSerializer): #serializers.ModelSerializer is a Django REST Framework 
    #class that auto-generates serializer fields from a model — simplifying conversion between model instances 
    # and JSON.
    id = serializers.UUIDField(source='public_id', read_only =True, format= 'hex') #creates a serializer 
    #field id that pulls its value from the model's public_id field (source='public_id'), formats the UUID as 
    # a hex string (format='hex') for easy readability in JSON. 
    created = serializers.DateTimeField(read_only= True)
    updated = serializers.DateTimeField(read_only= True)