import models
import presentation_layer

# Initialize database tables
models.create_tables()

# Run the application (GUI)
presentation_layer.run_application()
