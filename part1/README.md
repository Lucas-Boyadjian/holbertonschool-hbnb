# HBnB - UML Design Documentation

## Table of Contents
- [Project Overview](#project-overview)
- [Architecture Overview](#architecture-overview)
- [High-Level Package Diagram](#high-level-package-diagram)
- [Business Logic Layer](#business-logic-layer)
- [Entity Relationships](#entity-relationships)
- [Business Rules](#business-rules)
- [Design Decisions](#design-decisions)

## Project Overview
This project contains comprehensive UML documentation for the HBnB (Holberton Airbnb) application. These diagrams serve as architectural blueprints before development begins and ensure consistency across database design and business logic implementation.

## Architecture Overview
The HBnB application follows a layered architecture pattern with clear separation of concerns:
- **Presentation Layer**: User interface and API endpoints
- **Business Logic Layer**: Core entities and business rules
- **Data Access Layer**: Database operations and persistence

## High-Level Package Diagram
*[Your package diagram will go here]*

## Business Logic Layer

### Overview
The business logic layer contains the core domain entities that represent the fundamental concepts of our rental platform.

### Core Entities

#### User (ModelUser)
Represents platform users who can list properties and write reviews.
- **Key Attributes**: Unique identifier, personal information, authentication data
- **Capabilities**: Create, update, and delete user profiles
- **Security**: Password is private, admin status controls access levels

#### Place (ModelPlace)
Represents user feedback and ratings for places.
- **Key Attributes**: Rating (numeric), written comment, timestamps
- **Relationships**: Written by a User about a specific Place
- **Business Rule**: Must be associated with both a User and a Place

#### Amenity (ModelAmenity)
Represents facilities and services available at places.
- **Key Attributes**: Name, description, management timestamps
- **Relationship**: Many-to-many with Places through Place_amenity

#### Place_amenity (ModelPlace_amenity)
Junction table managing the manu-to-many relationship between Places and Amenities.

### Class Diagram
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

## Entity Relationships

### Relationship Details
- **User -> Place**: One-to-Many (1:0..*)
  - A user can own multiple properties
  - Each place must have exactly one owner

- **Place -> Review**: One-to-Many (1:0..*)
  - A Place can have multiple reviews
  - Each review belongs to exactly one place

- **User -> Review**: One-to_Many (1:0..*)
  - A user can write multiple reviews
  - Each review is written by exactly one user

- **Place <-> Amenity**: Many-toMany (via Place_amenity)
  - Places can have multiple amenities
  - Amenities can be shared across multiple palces

## Business Rules

### Data Integrity Constraints
1. **Referential Integrity**: All Foreign key relationships must be maintained
2. **User Dependency**: Places and Reviews cannot exist without valid User references
3. **Place Dependency**: Reviews cannot exist without valid Place references

### Business Logic Rules
1. **Authentication Required**: Only authenticated users can create places or reviews
2. **Ownership Rights**: Only place owners can modify their property details
3. **Review Limitations**: Users cannot review their own properties
4. **Amenity Reusability**: Amenities are shared resources across the platform

## Design Decisions

### Identifier Strategy
- **UUID4**: Used for all primary keys ro ensure global uniqueness and security
- **Benefits**: Prevents enumeration attacks, enables distributed systems

### Identifier Strategy
- **UUID4**: Used for all primary keys to ensure global uniqueness and security
- **Benefits**: Prevents enumeration attacks, enables distributed systems

### Timestamp Management
- **Automatic Timestamps**: Creation and update times are system-managed
- **Consistency**: All entities follow the same temporal tracking pattern

### Data Types
- **Coordinates**: Integer type for latitude/longitude (consider decimal precision needs)
- **Pricing**: Float type for monetary values (consider precision requirements)
- **Ratings**: Integer type for simplicity (1-5 scale assumed)

## Future Considerations
- Consider adding validation rules for ratings (1-5 range)
- Evaluate coordinate precision requirements for mapping accuracy
- Plan for soft delete functionality to maintain data history
- Consider adding audit trails for sensitive operations

## Conventions Used
- **Naming**: snake_case for attributes, PascalCase for classes
- **Visibility**: + (public), - (private) indicators
- **Prefixes**: "Model" prefix for all entity classes
- **Methods**: CRUD operations follow consistent naming patterns