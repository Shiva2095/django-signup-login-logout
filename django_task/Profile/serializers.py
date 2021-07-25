import re
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

    def validate_phone_number(self, mobile):
        if re.match(r'[6789]\d{9}$', mobile):
            return mobile
        else:
            raise serializers.ValidationError(
                "Please enter valid mobile number")
    
    # def create(self, validated_data):
    #     user = super(ProfileSerializer, self).create(validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user


