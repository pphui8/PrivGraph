import pickle
from matplotlib import pyplot as plt
import networkx as nx

if __name__ == "__main__":
    G = nx.DiGraph()
    G.add_node("direct_identifier", color="#336600")
    G.add_node("quasi_identifier", color="#336600")

    G.add_node("basic_information", color="#4D9900") # 66CC00 99FF33 CCFF99
    G.add_node("contact_information", color="#4D9900")
    G.add_node("official_information", color="#4D9900")
    G.add_edge("direct_identifier", "basic_information", color="#FF66B3", type="subsume")
    G.add_edge("direct_identifier", "contact_information", color="#FF66B3", type="subsume")
    G.add_edge("direct_identifier", "official_information", color="#FF66B3", type="subsume")

    G.add_node("name", color="#66CC00")
    G.add_node("date_of_birth", color="#66CC00")
    G.add_node("gender", color="#66CC00")
    G.add_node("marital_status", color="#66CC00")
    G.add_node("nationality", color="#66CC00")
    G.add_node("age", color="#66CC00")
    G.add_edge("basic_information", "name", color="#FF66B3", type="subsume")
    G.add_edge("basic_information", "date_of_birth", color="#FF66B3", type="subsume")
    G.add_edge("basic_information", "gender", color="#FF66B3", type="subsume")
    G.add_edge("basic_information", "marital_status", color="#FF66B3", type="subsume")
    G.add_edge("basic_information", "nationality", color="#FF66B3", type="subsume")
    G.add_edge("basic_information", "age", color="#FF66B3", type="subsume")

    G.add_node("home_address", color="#66CC00")
    G.add_node("email_address", color="#66CC00")
    G.add_node("phone_number", color="#66CC00")
    G.add_edge("contact_information", "home_address", color="#FF66B3", type="subsume")
    G.add_edge("contact_information", "email address", color="#FF66B3", type="subsume")
    G.add_edge("contact_information", "phone_number", color="#FF66B3", type="subsume")

    G.add_node("personal_ID", color="#66CC00")
    G.add_node("driver_license_ID", color="#66CC00")
    G.add_node("tax_identification_ID", color="#66CC00")
    G.add_node("student_ID", color="#66CC00")
    G.add_edge("official_information", "personal_ID", color="#FF66B3", type="subsume")
    G.add_edge("official_information", "driver_license_ID", color="#FF66B3", type="subsume")
    G.add_edge("official_information", "tax_identification_ID", color="#FF66B3", type="subsume")
    G.add_edge("official_information", "student_ID", color="#FF66B3", type="subsume")

    # extra leaf nodes
    G.add_node("identity_number", color="#CCFF99")
    G.add_node("social_security_number", color="#CCFF99")
    G.add_node("passport_number", color="#CCFF99")
    G.add_edge("personal_ID", "identity_number", color="#FF66B3", type="subsume")
    G.add_edge("personal_ID", "social_security_number", color="#FF66B3", type="subsume")
    G.add_edge("personal_ID", "passport_number", color="#FF66B3", type="subsume")

    G.add_node("location_data", color="#4D9900")
    G.add_node("online_identifiers", color="#4D9900")
    G.add_node("physiological_data", color="#4D9900")
    G.add_node("social_data", color="#4D9900")
    G.add_edge("quasi_identifier", "location_data", color="#FF66B3", type="subsume")
    G.add_edge("quasi_identifier", "online_identifiers", color="#FF66B3", type="subsume")
    G.add_edge("quasi_identifier", "physiological_data", color="#FF66B3", type="subsume")
    G.add_edge("quasi_identifier", "social_data", color="#FF66B3", type="subsume")

    G.add_node("GPS_coordinates", color="#66CC00")
    G.add_node("work_place", color="#66CC00")
    G.add_node("travel_history", color="#66CC00")
    G.add_node("zip_code", color="#66CC00")
    G.add_edge("location_data", "GPS_coordinates", color="#FF66B3", type="subsume")
    G.add_edge("location_data", "work_place", color="#FF66B3", type="subsume")
    G.add_edge("location_data", "travel_history", color="#FF66B3", type="subsume")
    G.add_edge("location_data", "zip_code", color="#FF66B3", type="subsume")

    G.add_node("IP_address", color="#66CC00")
    G.add_node("mac_address", color="#66CC00")
    G.add_node("cookies", color="#66CC00")
    G.add_node("username", color="#66CC00")
    G.add_edge("online_identifiers", "IP_address", color="#FF66B3", type="subsume")
    G.add_edge("online_identifiers", "mac_address", color="#FF66B3", type="subsume")
    G.add_edge("online_identifiers", "cookies", color="#FF66B3", type="subsume")
    G.add_edge("online_identifiers", "username", color="#FF66B3", type="subsume")

    G.add_node("biometric_data", color="#66CC00")
    G.add_node("health_records", color="#66CC00")
    G.add_edge("physiological_data", "biometric_data", color="#FF66B3", type="subsume")
    G.add_edge("physiological_data", "health_records", color="#FF66B3", type="subsume")

    # extra leaf nodes
    G.add_node("fingerprints", color="#CCFF99")
    G.add_node("facial_recognition_data", color="#CCFF99")
    G.add_node("iris_scans", color="#CCFF99")
    G.add_node("voice_records", color="#CCFF99")
    G.add_node("blood_type", color="#CCFF99")
    G.add_edge("biometric_data", "fingerprints", color="#FF66B3", type="subsume")
    G.add_edge("biometric_data", "facial_recognition_data", color="#FF66B3", type="subsume")
    G.add_edge("biometric_data", "iris_scans", color="#FF66B3", type="subsume")
    G.add_edge("biometric_data", "voice_records", color="#FF66B3", type="subsume")
    G.add_edge("biometric_data", "blood_type", color="#FF66B3", type="subsume")

    # etra leaf nodes
    G.add_node("illness_symptoms", color="#CCFF99")
    G.add_node("medical_diagnosis", color="#CCFF99")
    G.add_edge("health_records", "illness_symptoms", color="#FF66B3", type="subsume")
    G.add_edge("health_records", "medical_diagnosis", color="#FF66B3", type="subsume")

    
    G.add_node("religious_belifs", color="#66CC00")
    G.add_node("political_opinions", color="#66CC00")
    G.add_node("employment_history", color="#66CC00")
    G.add_node("education_background", color="#66CC00")
    G.add_node("financial_information", color="#66CC00")
    G.add_node("cultural_affillation", color="#66CC00")
    G.add_edge("social_data", "religious_belifs", color="#FF66B3", type="subsume")
    G.add_edge("social_data", "political_opinions", color="#FF66B3", type="subsume")
    G.add_edge("social_data", "employment_history", color="#FF66B3", type="subsume")
    G.add_edge("social_data", "education_background", color="#FF66B3", type="subsume")
    G.add_edge("social_data", "financial_information", color="#FF66B3", type="subsume")
    G.add_edge("social_data", "cultural_affillation", color="#FF66B3", type="subsume")

    # show the graph
    # pos = nx.spring_layout(G)
    # edge_colors = nx.get_edge_attributes(G, 'color')
    # node_colors = nx.get_node_attributes(G, 'color')
    # nx.draw_networkx(G, pos, edge_color=edge_colors.values(), node_color=node_colors.values(), with_labels=True)
    # plt.show()

    # save the graph
    with open("./output/Datatype.pkl", 'wb') as f:
        pickle.dump(G, f)