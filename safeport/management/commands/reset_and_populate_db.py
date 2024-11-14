from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
import psycopg2

class Command(BaseCommand):
    help = 'Drops all tables in the PostgreSQL database, makes migrations, and populates with a fixture.'

    def handle(self, *args, **kwargs):
        # Connect to the PostgreSQL database
        db_settings = settings.DATABASES['default']
        conn = psycopg2.connect(
            dbname=db_settings['NAME'],
            user=db_settings['USER'],
            password=db_settings['PASSWORD'],
            host=db_settings['HOST'],
            port=db_settings['PORT']
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Drop all tables
        self.stdout.write(self.style.WARNING("Dropping all tables..."))
        cursor.execute("""
            DO $$ DECLARE
                r RECORD;
            BEGIN
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
        """)
        cursor.close()
        conn.close()
        self.stdout.write(self.style.SUCCESS("All tables dropped."))

        # Apply migrations
        self.stdout.write(self.style.WARNING("Applying migrations..."))
        call_command('migrate')
        self.stdout.write(self.style.SUCCESS("Migrations applied successfully."))

        # Load data from a fixture
        self.stdout.write(self.style.WARNING("Loading fixture data..."))
        call_command('loaddata', 'initial_data.json') 
        self.stdout.write(self.style.SUCCESS("Fixture data loaded successfully."))