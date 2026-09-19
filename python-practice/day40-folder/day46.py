from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Integer,
    String,
    create_engine,
    Index,
    select,
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
    selectinload,
)

from sqlalchemy.exc import IntegrityError


# ============================================================
# DATABASE
# ============================================================

DATABASE_URL = "sqlite:///./day40.db"

engine = create_engine(
    DATABASE_URL,
    echo=True
)


# ============================================================
# BASE MODEL
# ============================================================

class Base(DeclarativeBase):
    pass


# ============================================================
# USER MODEL
# ============================================================

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True
    )

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="user"
    )

    projects: Mapped[list["Project"]] = relationship(
        back_populates="user"
    )


# ============================================================
# PROJECT MODEL
# ============================================================

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    user: Mapped["User"] = relationship(
        back_populates="projects"
    )

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="project"
    )


# ============================================================
# TASK MODEL
# ============================================================

class Task(Base):
    __tablename__ = "tasks"

    __table_args__ = (
        Index(
            "ix_tasks_user_id_completed",
            "user_id",
            "completed"
        ),
        CheckConstraint(
            "priority >= 1 AND priority <= 5",
            name="ck_tasks_priority_range"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    priority: Mapped[int] = mapped_column(
        Integer,
        default=3,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    due_date: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id"),
        nullable=True,
        index=True
    )

    user: Mapped["User"] = relationship(
        back_populates="tasks"
    )

    project: Mapped["Project | None"] = relationship(
        back_populates="tasks"
    )


# ============================================================
# PART 1 - CREATE CHECKPOINT DATA
# ============================================================

print("\n========== CREATING CHECKPOINT DATA ==========\n")

with Session(engine) as session:

    # Check whether checkpoint data already exists.
    existing_michael = session.scalar(
        select(User).where(
            User.email == "michael46@example.com"
        )
    )

    existing_sarah = session.scalar(
        select(User).where(
            User.email == "sarah46@example.com"
        )
    )

    if existing_michael is None and existing_sarah is None:

        michael = User(
            name="Michael",
            email="michael46@example.com"
        )

        sarah = User(
            name="Sarah",
            email="sarah46@example.com"
        )

        # ----------------------------------------------------
        # PROJECTS
        # ----------------------------------------------------

        backend_project = Project(
            name="Backend Engineering",
            user=michael
        )

        api_project = Project(
            name="API Project",
            user=michael
        )

        devops_project = Project(
            name="DevOps Project",
            user=sarah
        )

        # ----------------------------------------------------
        # MICHAEL'S TASKS
        # ----------------------------------------------------

        study_sqlalchemy = Task(
            title="Study SQLAlchemy",
            priority=5,
            user=michael,
            project=backend_project
        )

        practice_alembic = Task(
            title="Practice Alembic",
            priority=4,
            user=michael,
            project=backend_project
        )

        build_authentication = Task(
            title="Build Authentication",
            priority=5,
            user=michael,
            project=api_project
        )

        add_rate_limiting = Task(
            title="Add Rate Limiting",
            priority=3,
            user=michael,
            project=api_project
        )

        # ----------------------------------------------------
        # SARAH'S TASKS
        # ----------------------------------------------------

        learn_docker = Task(
            title="Learn Docker",
            priority=5,
            user=sarah,
            project=devops_project
        )

        study_ci_cd = Task(
            title="Study CI/CD",
            priority=4,
            user=sarah,
            project=devops_project
        )

        # Adding the Users is enough to persist the connected
        # object graph through relationship cascade.
        session.add_all([
            michael,
            sarah
        ])

        session.commit()

        print("Checkpoint data successfully created.")

    else:
        print("Checkpoint data already exists. Skipping seed.")


# ============================================================
# PART 2 - GET MICHAEL'S ID AND BACKEND PROJECT ID
# ============================================================

with Session(engine) as session:

    michael = session.scalar(
        select(User).where(
            User.email == "michael46@example.com"
        )
    )

    backend_project = session.scalar(
        select(Project)
        .join(Project.user)
        .where(
            User.email == "michael46@example.com",
            Project.name == "Backend Engineering"
        )
    )

    if michael is None:
        raise RuntimeError("Michael was not found.")

    if backend_project is None:
        raise RuntimeError(
            "Backend Engineering project was not found."
        )

    michael_id = michael.id
    backend_project_id = backend_project.id


# ============================================================
# PART 3 - ALL PROJECTS BELONGING TO MICHAEL
# ============================================================

print("\n========== MICHAEL'S PROJECTS ==========\n")

with Session(engine) as session:

    statement = (
        select(Project)
        .where(Project.user_id == michael_id)
    )

    michael_projects = session.scalars(
        statement
    ).all()

    for project in michael_projects:
        print(project.name)


# ============================================================
# PART 4 - TASKS IN BACKEND ENGINEERING
# ============================================================

print("\n========== BACKEND ENGINEERING TASKS ==========\n")

with Session(engine) as session:

    statement = (
        select(Task)
        .where(
            Task.project_id == backend_project_id
        )
    )

    tasks = session.scalars(statement).all()

    for task in tasks:
        print(
            f"{task.title} | Priority: {task.priority}"
        )


# ============================================================
# PART 5 - SARAH'S TASKS USING A JOIN
# ============================================================

print("\n========== SARAH'S TASKS ==========\n")

with Session(engine) as session:

    statement = (
        select(Task)
        .join(Task.project)
        .join(Project.user)
        .where(User.email == "sarah46@example.com")
    )

    tasks = session.scalars(statement).all()

    for task in tasks:
        print(
            f"{task.title} | Priority: {task.priority}"
        )


# ============================================================
# PART 6 - ALL HIGH PRIORITY TASKS
# ============================================================

print("\n========== ALL TASKS PRIORITY >= 4 ==========\n")

with Session(engine) as session:

    statement = (
        select(Task)
        .where(Task.priority >= 4)
    )

    tasks = session.scalars(statement).all()

    for task in tasks:
        print(
            f"{task.title} | Priority: {task.priority}"
        )


# ============================================================
# PART 7 - MICHAEL'S HIGH PRIORITY TASKS
# ============================================================

print("\n========== MICHAEL'S HIGH PRIORITY TASKS ==========\n")

with Session(engine) as session:

    statement = (
        select(Task)
        .where(
            Task.user_id == michael_id,
            Task.priority >= 4
        )
    )

    tasks = session.scalars(statement).all()

    for task in tasks:
        print(
            f"{task.title} | Priority: {task.priority}"
        )


# ============================================================
# PART 8 - RELATIONSHIP TRAVERSAL
# ============================================================

print("\n========== RELATIONSHIP TRAVERSAL ==========\n")

with Session(engine) as session:

    michael = session.scalar(
        select(User).where(
            User.email == "michael46@example.com"
        )
    )

    if michael is not None:

        print(f"User: {michael.name}")

        for project in michael.projects:

            print(f"\nProject: {project.name}")

            for task in project.tasks:

                print(
                    f"    Task: {task.title} "
                    f"| Priority: {task.priority}"
                )


# ============================================================
# PART 9 - EAGER LOADING WITH SELECTINLOAD
# ============================================================

print("\n========== EAGER LOADING ==========\n")

with Session(engine) as session:

    statement = (
        select(User)
        .options(
            selectinload(User.projects)
            .selectinload(Project.tasks)
        )
        .where(
            User.email == "michael46@example.com"
        )
    )

    michael = session.scalar(statement)

    if michael is not None:

        print(f"User: {michael.name}")

        for project in michael.projects:

            print(f"\nProject: {project.name}")

            for task in project.tasks:

                print(
                    f"    Task: {task.title}"
                )


# ============================================================
# PART 10 - INVALID PRIORITY CONSTRAINT TEST
# ============================================================

print("\n========== INVALID PRIORITY TEST ==========\n")

with Session(engine) as session:

    michael = session.scalar(
        select(User).where(
            User.email == "michael46@example.com"
        )
    )

    backend_project = session.scalar(
        select(Project)
        .join(Project.user)
        .where(
            User.email == "michael46@example.com",
            Project.name == "Backend Engineering"
        )
    )

    if michael is not None and backend_project is not None:

        invalid_task = Task(
            title="Impossible Priority",
            priority=20,
            user=michael,
            project=backend_project
        )

        try:
            session.add(invalid_task)
            session.commit()

            print(
                "ERROR: Invalid priority was accepted."
            )

        except IntegrityError:
            session.rollback()

            print(
                "SUCCESS: Database rejected priority 20."
            )


# ============================================================
# PART 11 - DUPLICATE EMAIL CONSTRAINT TEST
# ============================================================

print("\n========== DUPLICATE EMAIL TEST ==========\n")

with Session(engine) as session:

    duplicate_user = User(
        name="Fake Michael",
        email="michael46@example.com"
    )

    try:
        session.add(duplicate_user)
        session.commit()

        print(
            "ERROR: Duplicate email was accepted."
        )

    except IntegrityError:
        session.rollback()

        print(
            "SUCCESS: Database rejected duplicate email."
        )


# ============================================================
# PART 12 - TRANSACTION ATOMICITY TEST
# ============================================================

print("\n========== TRANSACTION ATOMICITY TEST ==========\n")

atomicity_test_title = "Atomicity Valid Task"

with Session(engine) as session:

    michael = session.scalar(
        select(User).where(
            User.email == "michael46@example.com"
        )
    )

    backend_project = session.scalar(
        select(Project)
        .join(Project.user)
        .where(
            User.email == "michael46@example.com",
            Project.name == "Backend Engineering"
        )
    )

    if michael is not None and backend_project is not None:

        valid_task = Task(
            title=atomicity_test_title,
            priority=3,
            user=michael,
            project=backend_project
        )

        invalid_task = Task(
            title="Atomicity Invalid Task",
            priority=99,
            user=michael,
            project=backend_project
        )

        try:

            session.add_all([
                valid_task,
                invalid_task
            ])

            session.commit()

            print(
                "ERROR: Transaction unexpectedly succeeded."
            )

        except IntegrityError:

            session.rollback()

            print(
                "Transaction failed because one Task "
                "violated the CHECK constraint."
            )


# ============================================================
# PART 13 - VERIFY ATOMICITY
# ============================================================

print("\n========== VERIFYING ATOMICITY ==========\n")

with Session(engine) as session:

    statement = (
        select(Task)
        .where(
            Task.title == atomicity_test_title
        )
    )

    task = session.scalar(statement)

    if task is None:

        print(
            "SUCCESS: The valid Task was also rolled back."
        )

        print(
            "The transaction was atomic."
        )

    else:

        print(
            "ERROR: The valid Task was inserted."
        )


# ============================================================
# PART 14 - SCHEMA EXPLANATION
# ============================================================

# ------------------------------------------------------------
# users.id
# ------------------------------------------------------------
#
# Table:
# users
#
# Type:
# Primary Key
#
# Purpose:
# Uniquely identifies each User.
#
# It is referenced by foreign keys such as:
#
# projects.user_id
# tasks.user_id


# ------------------------------------------------------------
# projects.user_id
# ------------------------------------------------------------
#
# Table:
# projects
#
# Type:
# Foreign Key
#
# References:
# users.id
#
# Purpose:
# Identifies which User owns the Project.


# ------------------------------------------------------------
# tasks.user_id
# ------------------------------------------------------------
#
# Table:
# tasks
#
# Type:
# Foreign Key
#
# References:
# users.id
#
# Purpose:
# Identifies the User directly associated with the Task.
#
# In this current schema it represents a direct User-to-Task
# relationship.


# ------------------------------------------------------------
# tasks.project_id
# ------------------------------------------------------------
#
# Table:
# tasks
#
# Type:
# Nullable Foreign Key
#
# References:
# projects.id
#
# Purpose:
# Identifies which Project the Task belongs to.
#
# Because it is nullable, a Task can currently exist without
# belonging to a Project.


# ============================================================
# MIGRATION CHECKPOINT
# ============================================================

# These commands should be run from the terminal:
#
# alembic current
#
# alembic history
#
#
# alembic current:
#
# Shows the migration revision currently applied to the
# database.
#
#
# alembic history:
#
# Shows the migration revision chain.
#
#
# The migration history should represent the evolution of the
# database schema rather than a collection of unrelated files.