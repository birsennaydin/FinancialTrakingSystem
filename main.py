import business_logic
import models
import presentation_layer

# Initialize database tables
models.create_tables()

# Insert default datas into tables
business_logic.insert_default_datas()

# Run the application (GUI)
presentation_layer.run_application()
