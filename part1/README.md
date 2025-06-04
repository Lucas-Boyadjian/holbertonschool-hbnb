# HBnB UML

This project contains all diagram for HBnB project

## High-Level Package Diagram

...

## Detailed Class Diagram for Business Logic Layer

In this diagram we have 5 class : `User`, `Place`, `Review`, `Place_amenity` and `Amenity`.

The `User` class can create a `Place`.

`Place` can have `Review` and `Amenity`.

`Place` can't exist `Userless`, `Review` can't exist `Placeless` and `Amenity` can't exist `Placeless` too.

```mermaid
---
config:
  theme: neo
  look: neo
  layout: elk
title: Business Logic Layer
---
classDiagram
direction LR
    class ModelUser {
	    +str UUID4 id
	    +str First_name
	    +str Last_name
	    +str email
	    -str password
	    -bool is_admin
	    +int date_time create_user
	    +int date_time update_user
	    +str update_user()
	    +str create_user()
	    +str delete_user()
    }
    class ModelPlace {
	    +str UUID4 id
	    +str UUID4 id_user
	    +str title
	    +str description
	    +float price
	    +int latitude
	    +int longitude
	    +int date_time create_place
	    +int date_time update_place
	    +list list_aminity()
	    +str create_place()
	    +str update_place()
	    +str delete_place()
	    +list list_place()
    }
    class ModelReview {
	    +str UUID4 id
	    +str UUID4 id_user
	    +str UUID4 id_place
	    +int rating
	    +str comment
	    +int date_time create_review
	    +int date_time update_review
	    +str create_review()
	    +str update_review()
	    +str delete_review()
	    +list list_aminity()
    }
    class ModelPlace_amenity {
	    +str UUID4 id
	    +str UUID4 id_place
	    +str UUID4 id_amenity
    }
    class ModelAmenity {
	    +str UUID4 id
	    +str name
	    +str description
	    +int date_time create_amenity
	    +int date_time update_amenity
	    +str create_amenity()
	    +str update_amenity()
	    +str delete_amenity()
	    +list list_aminity()
    }
    ModelUser "1" *--> "0..*¨" ModelPlace : owns
    ModelPlace "1" *--> "0..*" ModelReview : has
    ModelPlace "1" *--> "0..*" ModelPlace_amenity : contains
    ModelPlace_amenity "0..*" <-- "1" ModelAmenity
```