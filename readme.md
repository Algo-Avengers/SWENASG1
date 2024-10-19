# Student Conduct Tracker CLI

The Student Conduct Tracker is a Flask-based application that provides a command-line interface (CLI) for managing student reviews and user accounts. 

## Commands

### User Commands
- **Create a User**: `flask user create <username> <password>` (e.g., `flask user create rob robpass`)
- **List Users**: `flask user list [format]` (e.g., `flask user list json`)

### Student Commands
- **Add a Student**: `flask student add_student <student_id> <first_name> <last_name> <student_programme> <student_faculty>` (e.g., `flask student add_student 1234 Jake Blue "Computer Science" FST`)
- **Search for a Student**: `flask student search_student <student_id>` (e.g., `flask student search_student 1234`)

### Review Commands
- **Add a Review for a Student**: `flask review add_review <student_id> <staff_id> <review_type> <course> <comment>` (e.g., `flask review add_review 1234 1000 "positive" "COMP 3613" "Good Student."`)
- **View Reviews for a Specific Student**: `flask review view_reviews <student_id>` (e.g., `flask review view_reviews 1234`)

### Testing Commands
- **Run User Tests**: `flask test user [type]` where `type` can be `all`, `unit`, or `int` (e.g., `flask test user all` to run all tests).