# Implementation Plan: Car Research Platform

## Overview

This implementation plan builds upon the completed database setup (SQLite with 6 tables and sample data). The focus is on creating the backend API with Gemini AI integration, followed by the Next.js frontend for user interaction. The system will provide AI-powered car recommendations based on user preferences.

## Tasks

- [ ] 1. Create Pydantic schemas for API request/response validation
  - [ ] 1.1 Create schemas for car data models (Make, Model, Variant)
    - Define `MakeSchema`, `ModelSchema`, `VariantSchema` with all fields
    - Add nested schemas for dimensions and mileage
    - Include validation rules matching database constraints
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 8.3, 8.4, 8.5_
  
  - [ ] 1.2 Create schemas for user and preference profile models
    - Define `UserSchema`, `PreferenceProfileSchema` with validation
    - Add enums for priority levels (low/medium/high)
    - Validate budget_min < budget_max constraint
    - Validate numerical ranges (commute_distance, highway_city_ratio, passenger_count)
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.6, 2.7_
  
  - [ ] 1.3 Create schemas for recommendation responses
    - Define `RecommendationSchema` with confidence_score and match_explanation
    - Define `ShortlistResponseSchema` with list of recommendations
    - Add validation for confidence_score range (0-100)
    - _Requirements: 3.2, 3.3, 4.1_
  
  - [ ]* 1.4 Write unit tests for schema validation
    - Test valid and invalid inputs for each schema
    - Test constraint validation (budget, ranges, enums)
    - Test nested schema serialization
    - _Requirements: 2.6, 2.7, 8.3, 8.4, 8.5_

- [ ] 2. Implement Gemini API client integration
  - [ ] 2.1 Create gemini_client.py module
    - Configure Google Generative AI SDK with API key from environment
    - Create `GeminiClient` class with `generate_recommendations` method
    - Implement prompt engineering for car recommendations
    - Add JSON parsing and validation for AI responses
    - _Requirements: 3.1, 3.2, 4.2, 4.3, 4.5_
  
  - [ ] 2.2 Implement rate limiting and caching
    - Add request rate limiter (15 requests/minute for free tier)
    - Implement LRU cache for identical preference profiles
    - Add cache TTL configuration via environment variables
    - _Requirements: 9.1_
  
  - [ ] 2.3 Add fallback strategy for API failures
    - Implement rule-based scoring as fallback
    - Calculate score based on price match, mileage, and safety rating
    - Generate basic explanation templates
    - Log errors when falling back to rule-based system
    - _Requirements: 3.1, 3.2, 4.1_
  
  - [ ]* 2.4 Write unit tests for Gemini client
    - Mock Gemini API responses
    - Test prompt generation with various preference profiles
    - Test JSON parsing and error handling
    - Test fallback strategy activation
    - _Requirements: 3.1, 3.2, 4.1_

- [ ] 3. Checkpoint - Verify schemas and Gemini client
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 4. Implement recommendation engine with SQL pre-filtering
  - [ ] 4.1 Create recommendation_engine.py module
    - Implement `filter_candidates` function for SQL pre-filtering
    - Apply budget range filter (budget_min <= price <= budget_max)
    - Apply fuel type constraint filter
    - Apply transmission preference filter
    - Apply brand exclusions filter
    - Limit results to 50 candidates maximum
    - _Requirements: 3.4, 3.5, 6.2, 6.3_
  
  - [ ] 4.2 Implement recommendation generation workflow
    - Create `generate_recommendations` function
    - Call SQL pre-filter to get candidates
    - Format preference profile and candidates for Gemini prompt
    - Call Gemini API to score and rank candidates
    - Parse AI response and extract top 3-10 recommendations
    - Store recommendations in shortlists table
    - _Requirements: 3.1, 3.2, 3.3, 3.6, 3.7_
  
  - [ ] 4.3 Add configuration support for recommendation parameters
    - Load configuration from environment variables
    - Support MIN_RECOMMENDATIONS and MAX_RECOMMENDATIONS settings
    - Support MAX_CANDIDATE_CARS setting
    - Support GEMINI_MODEL and GEMINI_TEMPERATURE settings
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_
  
  - [ ]* 4.4 Write integration tests for recommendation engine
    - Test end-to-end recommendation generation with sample data
    - Test SQL pre-filtering with various constraints
    - Test empty shortlist scenario when no matches exist
    - Test configuration parameter changes
    - _Requirements: 3.1, 3.6, 3.7, 10.5_

- [ ] 5. Implement FastAPI routes for car data endpoints
  - [ ] 5.1 Create routes/cars.py with car data endpoints
    - Implement `GET /api/v1/cars` with query parameters (make, model, fuel_type, transmission, min_price, max_price, min_safety_rating)
    - Implement `GET /api/v1/cars/{variant_id}` for single car details
    - Implement `GET /api/v1/makes` to list all makes
    - Implement `GET /api/v1/models?make_id={make_id}` to list models for a make
    - Add database indexing queries for performance
    - Return results within 1 second for searches, 500ms for details
    - _Requirements: 1.6, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 9.2, 9.3, 9.4, 9.5_
  
  - [ ]* 5.2 Write unit tests for car data endpoints
    - Test query parameter filtering
    - Test pagination and sorting
    - Test error handling for invalid IDs
    - Test response time requirements
    - _Requirements: 6.1, 6.2, 6.3, 9.2, 9.3, 9.4_

- [ ] 6. Implement FastAPI routes for recommendations
  - [ ] 6.1 Create routes/recommendations.py with recommendation endpoints
    - Implement `POST /api/v1/recommendations` accepting PreferenceProfile
    - Call recommendation engine to generate shortlist
    - Return shortlist with confidence scores and explanations
    - Implement `GET /api/v1/recommendations/{profile_id}` to retrieve saved shortlist
    - Ensure response time within 2 seconds
    - _Requirements: 3.1, 3.2, 3.3, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 5.1, 9.1_
  
  - [ ]* 6.2 Write integration tests for recommendation endpoints
    - Test POST with valid preference profile
    - Test GET for existing shortlist
    - Test error handling for invalid profiles
    - Test response time requirements
    - _Requirements: 3.1, 3.6, 3.7, 9.1_

- [ ] 7. Implement FastAPI routes for users and profiles
  - [ ] 7.1 Create routes/users.py with user management endpoints
    - Implement `POST /api/v1/users` to create user with email
    - Implement `POST /api/v1/profiles` to create preference profile
    - Implement `GET /api/v1/profiles/{profile_id}` to retrieve profile
    - Implement `PUT /api/v1/profiles/{profile_id}` to update profile
    - Implement `GET /api/v1/users/{user_id}/profiles` to list user's profiles
    - Implement `GET /api/v1/users/{user_id}/shortlists` to list user's shortlists
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_
  
  - [ ]* 7.2 Write unit tests for user and profile endpoints
    - Test user creation and retrieval
    - Test profile CRUD operations
    - Test profile update triggers shortlist regeneration
    - Test error handling for invalid user/profile IDs
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_

- [ ] 8. Checkpoint - Verify all backend routes
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 9. Create FastAPI main application with middleware
  - [ ] 9.1 Create api/main.py with FastAPI app setup
    - Initialize FastAPI app with title and version
    - Configure CORS middleware with allowed origins from environment
    - Add request logging middleware
    - Register all route modules (cars, recommendations, users)
    - Add global exception handlers
    - Add health check endpoint `GET /health`
    - _Requirements: 8.6, 9.1, 9.2, 9.3, 9.4_
  
  - [ ] 9.2 Create environment configuration module
    - Load all environment variables (DATABASE_URL, GEMINI_API_KEY, CORS_ORIGINS)
    - Validate required environment variables on startup
    - Provide default values for optional settings
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_
  
  - [ ]* 9.3 Write integration tests for main app
    - Test CORS configuration
    - Test health check endpoint
    - Test global error handling
    - Test environment variable loading
    - _Requirements: 8.6_

- [ ] 10. Implement data import functionality
  - [ ] 10.1 Create routes/admin.py with admin endpoints
    - Implement `POST /api/v1/admin/cars/import` accepting JSON array
    - Parse JSON car data into database models
    - Validate all required fields before insertion
    - Return import summary (success count, error count, errors list)
    - _Requirements: 11.1, 11.2, 11.3, 11.6_
  
  - [ ] 10.2 Create specification parser module
    - Implement `parse_car_json` function
    - Validate required fields (make, model, variant, price, fuel_type)
    - Create Make, Model, and Variant records
    - Handle duplicate entries gracefully
    - Return descriptive errors for invalid data
    - _Requirements: 11.1, 11.2, 11.3, 11.6_
  
  - [ ] 10.3 Create specification formatter module
    - Implement `format_car_to_json` function
    - Convert Car_Record objects to JSON format
    - Ensure round-trip consistency (parse → format → parse)
    - _Requirements: 11.4, 11.5_
  
  - [ ]* 10.4 Write unit tests for import and parser
    - Test valid JSON import
    - Test invalid JSON handling
    - Test round-trip property (parse → format → parse)
    - Test duplicate handling
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

- [ ] 11. Create Next.js frontend project structure
  - [ ] 11.1 Initialize Next.js project with TypeScript and Tailwind CSS
    - Create frontend directory with Next.js 14+ (App Router)
    - Install dependencies (React 18+, TypeScript, Tailwind CSS)
    - Configure Tailwind CSS
    - Create basic layout with header and footer
    - _Requirements: 5.1_
  
  - [ ] 11.2 Create API client utility
    - Create `lib/api-client.ts` with fetch wrapper
    - Add base URL configuration from environment variable
    - Add error handling and response parsing
    - Create typed functions for each backend endpoint
    - _Requirements: 5.1, 8.6_

- [ ] 12. Implement preference form pages
  - [ ] 12.1 Create multi-step preference form
    - Create `app/preferences/page.tsx` with step navigation
    - Implement BudgetStep component (budget_min, budget_max)
    - Implement UsageStep component (commute_distance, highway_city_ratio, passenger_count)
    - Implement PrioritiesStep component (fuel_eff, safety, performance, comfort)
    - Implement ConstraintsStep component (fuel_type, transmission, brand_exclusions)
    - Add form validation matching backend schema
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.6, 2.7_
  
  - [ ] 12.2 Implement form submission and navigation
    - Add state management for form data across steps
    - Implement step navigation (next, previous, submit)
    - Call `POST /api/v1/recommendations` on form submission
    - Navigate to recommendations page on success
    - Display error messages on validation failure
    - _Requirements: 3.1, 8.6_
  
  - [ ]* 12.3 Write component tests for preference form
    - Test form validation rules
    - Test step navigation
    - Test form submission
    - Test error handling
    - _Requirements: 2.6, 2.7, 8.6_

- [ ] 13. Checkpoint - Verify preference form functionality
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 14. Implement recommendations display page
  - [ ] 14.1 Create recommendations page
    - Create `app/recommendations/page.tsx`
    - Display shortlist with confidence scores
    - Create ShortlistCard component showing car image, name, price, key specs
    - Display match explanation for each car
    - Highlight confidence score with visual indicator
    - Add "View Details" button for each car
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 5.1_
  
  - [ ] 14.2 Add shortlist interaction features
    - Implement checkbox selection for comparison
    - Add "Compare Selected" button (enabled when 2+ cars selected)
    - Add "Remove from Shortlist" button for each car
    - Add "Save Shortlist" button
    - Display empty state when no recommendations exist
    - Show suggestions to relax constraints when shortlist is empty
    - _Requirements: 3.7, 5.2, 5.5, 5.6_
  
  - [ ]* 14.3 Write component tests for recommendations page
    - Test shortlist rendering
    - Test car selection for comparison
    - Test remove from shortlist
    - Test empty state display
    - _Requirements: 3.7, 5.1, 5.5_

- [ ] 15. Implement car comparison page
  - [ ] 15.1 Create comparison page
    - Create `app/recommendations/compare/page.tsx`
    - Display selected cars in side-by-side columns
    - Create ComparisonTable component with aligned specification rows
    - Highlight differences between cars
    - Display price, mileage, safety rating, dimensions, and features
    - Add "Back to Shortlist" button
    - _Requirements: 5.2, 5.3, 5.4_
  
  - [ ]* 15.2 Write component tests for comparison page
    - Test side-by-side display
    - Test difference highlighting
    - Test navigation back to shortlist
    - _Requirements: 5.2, 5.3, 5.4_

- [ ] 16. Implement browse and search functionality
  - [ ] 16.1 Create browse cars page
    - Create `app/cars/page.tsx` with filter sidebar
    - Implement FilterSidebar component (price, fuel_type, transmission, safety_rating, mileage)
    - Implement CarGrid component displaying all cars
    - Call `GET /api/v1/cars` with filter parameters
    - Display matching car count
    - Add "Clear Filters" button
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7_
  
  - [ ] 16.2 Add search functionality
    - Add search input for make, model, or variant name
    - Implement debounced search to reduce API calls
    - Update results as filters and search change
    - Display loading state during search
    - _Requirements: 6.1, 6.5_
  
  - [ ]* 16.3 Write component tests for browse page
    - Test filter application
    - Test search functionality
    - Test clear filters
    - Test loading states
    - _Requirements: 6.1, 6.2, 6.3, 6.7_

- [ ] 17. Implement car detail page
  - [ ] 17.1 Create car detail page
    - Create `app/cars/[id]/page.tsx`
    - Call `GET /api/v1/cars/{variant_id}` to fetch car details
    - Display full specifications in SpecsTable component
    - Display car images in ImageGallery component (placeholder for now)
    - Show make, model, variant, price, and all specifications
    - Add "Add to Comparison" button
    - Add "Back to Browse" button
    - _Requirements: 1.6, 5.1_
  
  - [ ]* 17.2 Write component tests for car detail page
    - Test data fetching and display
    - Test error handling for invalid car ID
    - Test navigation buttons
    - _Requirements: 1.6, 8.6_

- [ ] 18. Implement user profile and history pages
  - [ ] 18.1 Create profile page
    - Create `app/profile/page.tsx`
    - Call `GET /api/v1/users/{user_id}/profiles` to list saved profiles
    - Call `GET /api/v1/users/{user_id}/shortlists` to list saved shortlists
    - Display list of saved preference profiles with edit/delete buttons
    - Display list of saved shortlists with view button
    - Add "Create New Profile" button
    - _Requirements: 7.2, 7.3, 7.4_
  
  - [ ] 18.2 Implement profile editing
    - Add edit functionality for saved profiles
    - Call `PUT /api/v1/profiles/{profile_id}` to update profile
    - Regenerate shortlist when profile is updated
    - Navigate to updated shortlist on save
    - _Requirements: 7.5, 7.6_
  
  - [ ]* 18.3 Write component tests for profile page
    - Test profile list display
    - Test profile editing
    - Test shortlist regeneration on update
    - _Requirements: 7.3, 7.4, 7.5, 7.6_

- [ ] 19. Checkpoint - Verify all frontend functionality
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 20. Create landing page and navigation
  - [ ] 20.1 Create landing page
    - Create `app/page.tsx` with hero section
    - Add "Find My Car" CTA button linking to /preferences
    - Add "Browse All Cars" button linking to /cars
    - Add feature highlights section
    - Add responsive design with Tailwind CSS
    - _Requirements: 5.1_
  
  - [ ] 20.2 Implement navigation header
    - Create Header component with navigation links
    - Add links to Home, Browse Cars, Profile
    - Add responsive mobile menu
    - Style with Tailwind CSS
    - _Requirements: 5.1_

- [ ] 21. Configure deployment for Vercel
  - [ ] 21.1 Create Vercel configuration for backend
    - Create `backend/vercel.json` for serverless functions
    - Configure Python runtime and dependencies
    - Set up environment variables in Vercel dashboard
    - Configure CORS origins for production
    - _Requirements: 9.1_
  
  - [ ] 21.2 Create Vercel configuration for frontend
    - Create `frontend/next.config.js` with API URL configuration
    - Set up environment variables for production
    - Configure build settings
    - _Requirements: 5.1_
  
  - [ ] 21.3 Create deployment documentation
    - Document environment variables needed
    - Document deployment steps for Vercel
    - Document database setup (SQLite file or Turso migration)
    - Add troubleshooting guide
    - _Requirements: 9.1_

- [ ] 22. Final integration testing and polish
  - [ ] 22.1 Test complete user flow end-to-end
    - Test new user → preference form → recommendations → comparison → save
    - Test browse → filter → search → car detail
    - Test profile → edit → regenerate shortlist
    - Verify all API endpoints work correctly
    - _Requirements: 3.1, 5.1, 6.1, 7.1_
  
  - [ ] 22.2 Add error handling and loading states
    - Add loading spinners for all async operations
    - Add error messages for API failures
    - Add empty states for all list views
    - Add form validation error messages
    - _Requirements: 8.6_
  
  - [ ] 22.3 Optimize performance
    - Verify API response times meet requirements
    - Add database query optimization if needed
    - Add frontend code splitting
    - Optimize images and assets
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ] 23. Final checkpoint - Complete system verification
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Database setup is already complete (SQLite with 6 tables and sample data)
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at key milestones
- Backend uses Python FastAPI with SQLAlchemy ORM
- Frontend uses Next.js 14+ with TypeScript and Tailwind CSS
- AI recommendations powered by Google Gemini API
- Deployment target is Vercel for both frontend and backend
- Testing focuses on unit tests and integration tests (no property-based tests needed for this application type)

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2", "1.3"] },
    { "id": 1, "tasks": ["1.4", "2.1"] },
    { "id": 2, "tasks": ["2.2", "2.3"] },
    { "id": 3, "tasks": ["2.4", "4.1"] },
    { "id": 4, "tasks": ["4.2", "4.3"] },
    { "id": 5, "tasks": ["4.4", "5.1", "10.1", "10.2", "10.3"] },
    { "id": 6, "tasks": ["5.2", "6.1", "10.4"] },
    { "id": 7, "tasks": ["6.2", "7.1"] },
    { "id": 8, "tasks": ["7.2", "9.1", "9.2"] },
    { "id": 9, "tasks": ["9.3", "11.1"] },
    { "id": 10, "tasks": ["11.2", "12.1"] },
    { "id": 11, "tasks": ["12.2"] },
    { "id": 12, "tasks": ["12.3", "14.1"] },
    { "id": 13, "tasks": ["14.2"] },
    { "id": 14, "tasks": ["14.3", "15.1", "16.1"] },
    { "id": 15, "tasks": ["15.2", "16.2"] },
    { "id": 16, "tasks": ["16.3", "17.1", "18.1"] },
    { "id": 17, "tasks": ["17.2", "18.2"] },
    { "id": 18, "tasks": ["18.3", "20.1", "20.2"] },
    { "id": 19, "tasks": ["21.1", "21.2", "21.3"] },
    { "id": 20, "tasks": ["22.1", "22.2", "22.3"] }
  ]
}
```
