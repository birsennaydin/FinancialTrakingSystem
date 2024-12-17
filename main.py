from business.database_setup import insert_default_datas
import models.models as models
import presentation_layer

# Initialize database tables
models.create_tables()

# Insert default datas into tables
insert_default_datas()

# Run the application (GUI)
presentation_layer.run_application()
