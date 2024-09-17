#Dependencies 
from flask import Flask, request, jsonify
from model import fetch_strava_data, preprocess_strava_data, format_query, generate_advice


app = Flask(__name__)

#when post request comes through go to advice function
@app.route('/advice', methods=['POST'])

def get_advice(): 

    #Get JSON data from incoming request
    data = request.json
    
    access_token = data.get('acess_token')

    if not access_token: 
        #The HTTP 400 Bad Request client error  indicates that the server would not process the request due to something the server considered to be a client error.
        return jsonify({'error': 'Acess Token is required'}), 400
    
    try: 
           # Fetch and process Strava data
        strava_data = fetch_strava_data(access_token)
        processed_data = preprocess_strava_data(strava_data)
        query = format_query(processed_data)

            # Generate and return advice
        advice = generate_advice(query)
        return jsonify({"advice": advice})


    except Exception as e: 
        return jsonify({"error": str(e)}), 500



#Name is set to main if the script is being run directily as opposed to imported in
if __name__ == '__main__':
    #Run the script
    app.run(debug=True)

