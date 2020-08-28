from django.contrib import admin
from .models import HouseRule, Amenity, RoomType, Room, Photo, Service


class PhotoInline(admin.TabularInline):
    model = Photo

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass

@admin.register(HouseRule)
class HouseRuleAdmin(admin.ModelAdmin):
    pass

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    pass

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = [PhotoInline,]

@admin.register(Service)
class Service(admin.ModelAdmin):
    pass

