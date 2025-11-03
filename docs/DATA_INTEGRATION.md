# ResQTrack Data Integration System

## Overview

ResQTrack now includes a comprehensive data integration system that allows you to import, manage, and visualize multiple real-world datasets for emergency response coordination. The system supports NGOs, volunteers, hospitals, police stations, blood banks, fire stations, and emergency contacts.

## Features

### 🗄️ Database Models
- **NGOs**: Non-governmental organizations for animal rescue
- **Volunteers**: Individual volunteers with expertise areas
- **Hospitals**: Animal hospitals and veterinary clinics
- **Police Stations**: Emergency police services
- **Blood Banks**: Blood donation and storage facilities
- **Fire Stations**: Fire and rescue services
- **Emergency Contacts**: General emergency contact directory

### 📊 Data Import/Export
- CSV file import for all entity types
- Data validation and error reporting
- Duplicate detection and handling
- Export functionality for data backup
- Batch import with detailed statistics

### 🎯 API Endpoints
- RESTful API for all data operations
- JWT authentication for protected endpoints
- Public endpoints for emergency services
- Location-based service discovery
- Real-time statistics and analytics

### 📈 Visualization Dashboard
- Interactive data dashboard
- Real-time statistics cards
- Chart.js visualizations
- Location distribution maps
- Service type filtering

## Quick Start

### 1. Database Setup
```bash
# Apply database migrations
python -m flask --app backend/wsgi.py db upgrade
```

### 2. Import Sample Data
```bash
# Import all sample datasets
python import_sample_data.py

# Or import with data clearing
python import_sample_data.py --clear
```

### 3. Start the Server
```bash
# Backend API
python backend/wsgi.py

# Frontend (in another terminal)
cd frontend
python -m http.server 8000
```

### 4. Access the Dashboard
Visit `http://localhost:8000/data-dashboard.html` to access the data management interface.

## Data Import

### Supported CSV Formats

#### NGOs (`ngos.csv`)
```csv
name,email,phone,location,operating_zones,approved
Animal Rescue Foundation,contact@arf.org,+91-9876543210,Mumbai,"Mumbai,Thane,Navi Mumbai",true
```

#### Volunteers (`volunteers.csv`)
```csv
name,email,phone,location,expertise,availability,approved
John Smith,john.smith@email.com,+91-9876543215,Mumbai,pickup,weekends,true
```

#### Hospitals (`hospitals.csv`)
```csv
name,address,phone,location,is_24x7,treatment_types
Pet Hospital Mumbai,123 Marine Drive,Mumbai,+91-9876543220,Mumbai,true,"surgery,first aid,emergency"
```

#### Police Stations (`police_stations.csv`)
```csv
name,address,phone,location,station_code,is_24x7,jurisdiction,officer_in_charge
Mumbai Central Police Station,1 MG Road,Mumbai,+91-9876543225,Mumbai,MCP001,true,South Mumbai,Inspector Rajesh Kumar
```

#### Blood Banks (`blood_banks.csv`)
```csv
name,address,phone,location,is_24x7,blood_types_available,contact_person,license_number
Mumbai Blood Bank,123 Hospital Road,Mumbai,+91-9876543230,Mumbai,false,"A+,B+,O+,AB+",Dr. Rajesh Patel,BB001
```

#### Fire Stations (`fire_stations.csv`)
```csv
name,address,phone,location,station_code,is_24x7,equipment_available,chief_officer
Mumbai Fire Station,123 Fire Brigade Road,Mumbai,+91-9876543235,Mumbai,MFS001,true,"Fire trucks,Rescue equipment,Ladders",Chief Fire Officer Ravi Sharma
```

### Import Process
1. Navigate to the Data Dashboard
2. Select the appropriate CSV file
3. Click the Import button
4. Review import statistics and errors
5. Data is automatically validated and imported

## API Reference

### Authentication
Most endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

### Data Import Endpoints
- `POST /data/import/ngos` - Import NGOs from CSV
- `POST /data/import/volunteers` - Import Volunteers from CSV
- `POST /data/import/hospitals` - Import Hospitals from CSV
- `POST /data/import/police-stations` - Import Police Stations from CSV
- `POST /data/import/blood-banks` - Import Blood Banks from CSV
- `POST /data/import/fire-stations` - Import Fire Stations from CSV

### Data Export Endpoints
- `GET /data/export/ngos` - Export NGOs to CSV
- `GET /data/export/volunteers` - Export Volunteers to CSV
- `GET /data/export/hospitals` - Export Hospitals to CSV

### Analytics Endpoints
- `GET /data/statistics` - Get comprehensive statistics (requires auth)
- `GET /data/emergency-contacts` - Get emergency contacts (public)
- `GET /data/nearby-services?location=<location>&service_type=<type>` - Find nearby services (public)

### Example API Usage

#### Import NGOs
```bash
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -F "file=@ngos.csv" \
  http://localhost:5000/data/import/ngos
```

#### Get Statistics
```bash
curl -X GET \
  -H "Authorization: Bearer <token>" \
  http://localhost:5000/data/statistics
```

#### Find Nearby Services
```bash
curl -X GET \
  "http://localhost:5000/data/nearby-services?location=Mumbai&service_type=hospital"
```

## Data Validation

The system includes comprehensive data validation:

### Email Validation
- Basic format checking
- Duplicate detection
- Case normalization

### Phone Validation
- Minimum length requirements
- Format standardization

### Location Validation
- Minimum length requirements
- Geographic consistency

### Error Handling
- Detailed error reporting
- Row-by-row validation
- Skip vs. fail options
- Import statistics

## Frontend Dashboard

### Features
- **Statistics Cards**: Real-time counts of all entities
- **Import Interface**: Drag-and-drop CSV file uploads
- **Charts**: Service distribution and location analysis
- **Emergency Directory**: Searchable emergency contacts
- **Export Tools**: Download data in CSV format

### Navigation
- Accessible from main navigation menu
- Integrated with existing admin dashboard
- Responsive design for mobile devices

## Database Schema

### New Tables Added
- `police_stations` - Police station information
- `blood_banks` - Blood bank facilities
- `fire_stations` - Fire station services
- `emergency_contacts` - General emergency contacts

### Relationships
- All tables include timestamp tracking
- Location-based relationships
- Service type categorization
- Priority level assignments

## Security

### Authentication
- JWT-based authentication for admin operations
- Public endpoints for emergency services
- Role-based access control

### Data Protection
- Input validation and sanitization
- SQL injection prevention
- File upload security
- CORS configuration

## Performance

### Optimization
- Database indexing on location fields
- Efficient query patterns
- Pagination for large datasets
- Caching for statistics

### Scalability
- Modular architecture
- Horizontal scaling support
- Database migration system
- API versioning ready

## Troubleshooting

### Common Issues

#### Import Failures
- Check CSV format and headers
- Verify file encoding (UTF-8)
- Review validation errors
- Check database permissions

#### API Errors
- Verify JWT token validity
- Check endpoint URLs
- Review request format
- Monitor server logs

#### Dashboard Issues
- Clear browser cache
- Check JavaScript console
- Verify API connectivity
- Review CORS settings

### Debug Mode
Enable debug mode in `backend/config.py`:
```python
DEBUG = True
```

## Future Enhancements

### Planned Features
- Real-time data synchronization
- Advanced analytics and reporting
- Geographic mapping integration
- Mobile app API support
- Automated data validation rules
- Data quality scoring
- Integration with external APIs

### Extensibility
- Plugin architecture for new data sources
- Custom validation rules
- Advanced visualization options
- Multi-language support
- International data formats

## Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Code Standards
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comprehensive docstrings
- Include error handling
- Write unit tests

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Contact the development team
- Review the documentation
- Check the troubleshooting guide
