<<<<<<< HEAD
# 5SDBDproject

### Setting Up Environment Variables

To configure the application, you need to set up your environment variables in a .env file. A sample file .env.sample is provided in the repository. Follow these steps:

- Rename .env.sample to .env in the root directory of the project.
- Add Your Configuration Values:
        TISSEO_API_KEY: Your API key for accessing the Tisseo API.
        DATABASE: Your MongoDB connection string.
  
**Example:**
```env
TISSEO_API_KEY=your_api_key_here
DATABASE=mongodb+srv://username:password@cluster.mongodb.net/dbname
```
- Save the File:
Ensure that the .env file is saved in the root directory.


### Scheduler
The scheduler is implemented using GitHub Actions to automate the fetching and saving of data.

**Workflow Steps:**

- The script checks out the latest version of the code from the repository.
- Python is set up with the specified version (3.11).
- Dependencies are installed from requirements.txt.
- The API key and MongoDB credentials are securely passed as environment variables, and the script fetch_disruptions.py is executed to fetch and save data.
=======
This is a starter template for [Learn Next.js](https://nextjs.org/learn).
>>>>>>> bdf82cb (Initial commit from Create Next App)
