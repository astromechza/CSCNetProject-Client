import org.json.JSONArray;
import org.json.JSONObject;
import org.json.JSONStringer;



public class SensorClient {
	
	public static void main(String[] args) {

	    // First thing to do: ARG Parsing! (ye skurvy dogs)
	    
	        
	    // QUICK JSON EXAMPLE
	    JSONObject o = new JSONObject();
	    // add key values
        o.put("id", 0);
	    o.put("method", "ping");
	    String json = o.toString();
	    
	    //print out
	    System.out.println(json);
	    
	    // Super easy breakdown
	    JSONObject in = new JSONObject(json);
	    System.out.println("method = " + in.getString("method"));
	    System.out.println("id = "     + in.getInt("id")       );
	    
	    System.out.println();
	    
	    // COMPOSITE objects, ie: objects that contain other objects or arrays
	    JSONObject person = new JSONObject();
	    
    	    JSONObject params = new JSONObject();
    	    params.put("name", "John");
    	    params.put("surname", "Smith");
	    
        	    JSONArray marks = new JSONArray();
        	    marks.put(100);
        	    marks.put(200);
        	    marks.put(123.45);
	    
        	params.put("marks", marks);
	    
	    person.put("params", params);
	    
	    System.out.println(person.toString());

        // parse it in the same way
	    JSONObject result = new JSONObject(person.toString());
	    
	    // Can burrow down and cast to retrieve things
	    System.out.println(((JSONObject)result.get("params")).get("marks"));
	    
	    // ARRAYS
	    JSONArray a = (JSONArray) ( (JSONObject)result.get("params") ).get("marks");
	    
	    // get at position
	    System.out.println(a.getInt(2));   //specific type
	    System.out.println(a.get(0));      //general object
	    
	    
	    
	    
	}

}
