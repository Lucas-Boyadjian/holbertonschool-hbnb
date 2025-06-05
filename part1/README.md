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
```mermaid
classDiagram
direction TB
    class PresentationLayer {
	    +UserController
	    +PlaceController
	    +ReviewController
	    +AmenityController
    }

    class BusinessLogicLayer {
	    +UserClass
	    +PlaceClass
	    +ReviewClass
	    +AmenityClass
    }

    class PersistenceLayer {
	    +UserData
	    +PlaceData
	    +ReviewData
	    +AmenityData
    }

    PresentationLayer --> BusinessLogicLayer : Facade Pattern
    BusinessLogicLayer --> PersistenceLayer : DataBase operations
    PresentationLayer <.. BusinessLogicLayer
    BusinessLogicLayer <.. PersistenceLayer
```

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

### Sequence Diagrams for API Calls

### User Registration
```mermaid
---
config:
  theme: redux-dark-color
---
sequenceDiagram
  participant Interface as Interface (User)
  participant API as API (Presentation Layer)
  participant UserModel as UserModel (Business Logic Layer)
  participant UserRepository as UserRepository (Persistence Layer)
  participant Database as Database
  Interface ->>+ API: (1) POST /UserRegistration (JSON: e-mail, password)
  API ->>+ UserModel: (2) Validate user fields
  alt VALIDATION FAILED
    UserModel -->> API: (3) Error: invalid fields
    API -->> Interface: (4) 400 Bad Request (invalid fields)
  else VALIDATION SUCCESS
    UserModel -->> API: (5) Success: valid fields
    API ->> UserModel: (6) Request to create user (e-mail, password)
    UserModel ->>+ UserRepository: (7) Request a uniqueness check (e-mail)
    UserRepository ->>+ Database: (8) Search user by e-mail
    alt E-MAIL EXIST
      Database -->> UserRepository: (9) E-mail associated with a user
      UserRepository -->> UserModel: (10) Error: duplicate found
      UserModel -->> API: (11) Error: E-mail is already taken
      API -->> Interface: (12) 409 Conflict (e-mail already exist)
    else E-MAIL UNIQUE
      Database -->> UserRepository: (13) E-mail not found
      UserRepository -->> UserModel: (14) Success: e-mail is unique
      UserModel ->> UserModel: (15) Hash password
      UserModel ->> UserRepository: (16) Request to save user data (e-mail, hashed password)
      UserRepository ->> Database: (17) Insert user (as JSON)
      Database -->>- UserRepository: (18) Return: new user ID
      UserRepository -->>- UserModel: (19) Success: user data saved
      UserModel -->>- API: (20) User object creation (ID, e-mail)
      API -->>- Interface: (21) 201 Created (JSON: ID, e-mail)
    end
  end
```
This sequence diagram illustrates how a new user registers in the HBnB system:

1. **Request Submission**: User provides email and password credentials
2. **Input Validation**: System verifies that all required fields are properly formatted
3. **Duplicate Prevention**: System checks whether the email is already registered
4. **Secure Storage**: For new users, password is hashed before storage
5. **User Creation**: Valid user data is persisted in the database 
6. **Confirmation**: System responds with the new user's unique ID

Key aspects of this flow:
- Data validation happens before database operations
- Email uniqueness is enforced to prevent duplicate accounts
- Password security is maintained through hashing
- Only non-sensitive data is returned in the response (ID and email)
- Clear HTTP status codes indicate success (201) or specific failure reasons (400, 409)

This flow implements the principle of defense in depth, with multiple validation steps before creating a new user account.

### Place Creation
```mermaid
---
config:
  theme: redux-dark-color
---
sequenceDiagram
  participant Interface as Interface (User)
  participant API as API (Presentation Layer)
  participant AuthService as AuthService (Business Logic Layer)
  participant PlaceModel as PlaceModel (Business Logic Layer)
  participant PlaceRepository as PlaceRepository (Persistence Layer)
  participant Database as Database

  Interface ->>+ API: (1) POST /PlaceCreation (JSON: title, description, price, latitude, longitude)
  API ->>+ AuthService: (2) Validate token
  AuthService ->>+ Database: (3) Check token and get user

  alt INVALID TOKEN
    Database -->> AuthService: (4) Error: invalid token
    AuthService -->> API: (5) Return unauthorized
    API -->> Interface: (6) 401 Unauthorized (invalid token)
  else VALID TOKEN
    Database -->> AuthService: (7) Success: return UserID
    AuthService -->>- API: (8) Return authenticated (UserID)
    API ->>+ PlaceModel: (9) Validate place fields

    alt VALIDATION FAILED
      PlaceModel -->> API: (10) Error: invalid fields 
      API -->> Interface: (11) 400 Bad Request (invalid fields)
    else VALIDATION SUCCESS
      PlaceModel -->> API: (12) Success: valid fields
      API ->> PlaceModel: (13) Create place
      PlaceModel ->>+ PlaceRepository: (14) Save place
      PlaceRepository ->> Database: (15) Insert place (associated to the User)
      Database -->>- PlaceRepository: (16) Return place ID
      PlaceRepository -->>- PlaceModel: (17) Place saved
      PlaceModel -->>- API: (18) Return created place object
      API -->>- Interface: (19) 201 Created (JSON: title, description, price, latitude, longitude, userId, placeId)
    end
  end
```
This sequence diagram illustrates how an authenticated user creates a new place listing:

1. **Request Submission**: User submits place details (title, description, price, location)
2. **Authentication**: System validates the user's identity through token verification
3. **Data Validation**: Place details are validated against business rules
4. **Persistence**: Valid place data is stored in the database with user association
5. **Confirmation**: System responds with the newly created place details

Key aspects of this flow:
- Authentication verification occurs before any business logic processing
- Input validation ensures data integrity before persistence
- User-place relationship is established in the database
- Response includes both the place data and its unique identifier
- Clear HTTP status codes indicate success (201) or specific failure reasons (400, 401)

This flow enforces the "Authentication Required" business rule by ensuring only verified users can create place listings.

### Review Submission
```mermaid
---
config:
  theme: redux-dark-color
---
sequenceDiagram
  participant Interface as Interface (User)
  participant API as API (Presentation Layer)
  participant AuthService as AuthService (Business Logic Layer)
  participant ReviewModel as ReviewModel (Business Logic Layer)
  participant ReviewRepository as ReviewRepository (Persistence Layer)
  participant Database as Database

  Interface ->>+ API: (1) POST /ReviewSubmission (JSON: PlaceID, rating, comment)
  API ->>+ AuthService: (2) Validate token
  AuthService ->>+ Database: (3) Check token and get user

  alt INVALID TOKEN
    Database -->> AuthService: (4) Error: invalid token
    AuthService -->> API: (5) Return unauthorized
    API -->> Interface: (6) 401 Unauthorized (invalid token)
  else VALID TOKEN
    Database -->> AuthService: (7) Success: return UserID
    AuthService -->>- API: (8) Return authenticated (UserID)
    API ->>+ ReviewModel: (9) Validate review fields

    alt VALIDATION FAILED
      ReviewModel -->> API: (10) Error: invalid fields
      API -->> Interface: (11) 400 Bad Request (invalid fields)
    else VALIDATION SUCCESS
      ReviewModel -->> API: (12) Success: valid fields
      API ->> ReviewModel: (13) Create review
      ReviewModel ->>+ ReviewRepository: (14) Save review
      ReviewRepository ->> Database: (15) Insert review (associated to the Place)
      Database -->>- ReviewRepository: (16) Return review ID
      ReviewRepository -->>- ReviewModel: (17) Review saved
      ReviewModel -->>- API: (18) Return created review object
      API -->>- Interface: (19) 201 Created (JSON: PlaceID, rating, comment, UserID, ReviewID)
    end
  end
```
This sequence diagram illustrates how an authenticated user submits a review for a place:

1. **Request Submission**: User submits review details (place ID, rating, comment)
2. **Authentication**: System validates the user's identity through token verification
3. **Data Validation**: Review content is validated against business rules
4. **Persistence**: Valid review data is stored in the database with user and place associations
5. **Confirmation**: System responds with the newly created review details

Key aspects of this flow:
- Authentication verification occurs before any business logic processing
- Input validation ensures review data meets quality standards
- Both user-review and place-review relationships are established in the database
- Response includes the complete review data with all relevant identifiers
- Clear HTTP status codes indicate success (201) or specific failure reasons (400, 401)

This flow enforces both the "Authentication Required" business rule and establishes the necessary relationships required by the data integrity constraints.

### Fetching a List of Places
```mermaid
---
config:
  theme: redux-dark-color
---
sequenceDiagram
  participant Interface as Interface (User)
  participant API as API (Presentation Layer)
  participant AuthService as AuthService (Business Logic Layer)
  participant PlaceQueryModel as PlaceQueryModel (Business Logic Layer)
  participant PlaceRepository as PlaceRepository (Persistence Layer)
  participant Database as Database

  Interface ->>+ API: GET /FetchingListOfPlaces (filters)
  API ->>+ AuthService: Validate token
  AuthService ->>+ Database: Check token and get user
  alt INVALID TOKEN
    Database -->> AuthService: Error: invalid token
    AuthService -->> API: Error: unauthorized
    API -->> Interface: 401 unauthorized (invalid token)
  else VALID TOKEN
    Database -->> AuthService: Success: return UserID
    AuthService -->>- API: Return authenticated (UserID)
    API ->>+ PlaceQueryModel: Validate parameters
    alt VALIDATION FAILED
      PlaceQueryModel -->> API: Error: invalid parameters
      API -->> Interface: 400 Bad Request (invalid filters)
    else VALIDATION SUCCESS
      PlaceQueryModel -->> API: Valid parameters
      API ->> PlaceQueryModel: Fetch places matching filters
      PlaceQueryModel ->>+ PlaceRepository: Search places
      PlaceRepository ->> Database: Query places with filters
      Database -->>- PlaceRepository: Return matching places
      PlaceRepository -->>- PlaceQueryModel: Create list of matched places 
      PlaceQueryModel -->>- API: Return list of places
      API -->>- Interface: 200 list sorted (JSON: list of places)
    end
  end
```

### Place Listing Flow

This sequence diagram illustrates how an authenticated user fetches a filtered list of places:

1. **Request Submission**: User submits a request with optional filter parameters
2. **Authentication**: System validates the user's identity through token verification
3. **Parameter Validation**: Filter parameters are validated for correctness
4. **Data Retrieval**: System queries the database for places matching the filters
5. **Results Processing**: Matching places are collected and sorted according to criteria
6. **Confirmation**: System responds with the sorted list of places

Key aspects of this flow:
- Authentication verification ensures only authorized users can access listing data
- Parameter validation prevents invalid database queries
- Filtering capabilities enable users to find relevant properties
- Sorting functionality improves user experience and data organization
- Response includes complete listing information in a structured format
- Clear HTTP status codes indicate success (200) or specific failure reasons (400, 401)

This flow supports the core functionality of browsing available properties while maintaining system security through proper authentication.