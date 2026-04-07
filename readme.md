### cleanroom api 
Clean Room API is created for the management of schedules and tasks in non traditional grouping. Made for people who find calenders or todo list too cluttered or simple so they can find a solution that has the right amount of structure. Areas can be personal or shared across multiple users with role access. Tasks can be grouped, nested into subtasks, and scheduled as one time or recurring events.
___
#### Overview
Built to develop backend engineering skills. API design, relational databases, authentication, and scheduling logic. Personally I made this tool to solve my issues with other scheduling solutions. I struggle with consistently using calendar and todo apps, so I wanted something with the right amount of structure. I plan to continue building it out to better fit my needs.
___
#### Features
+ Auth0-protected endpoints with JWT verification
+ Multi-user areas with owner/member roles
+ Tasks with subtask hierarchies (parent/child)
+ Task groups for organizing tasks across areas
+ Schedules with optional recurrence (rrule-based)
+ Independent task and schedule status state machines
___
#### Made with:
+ FastAPI 
+ SQLAlchemy 2.0
+ PostgreSQL via (Supabase)
+ Alembic
+ Auth0 