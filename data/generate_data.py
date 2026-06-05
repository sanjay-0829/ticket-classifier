import pandas as pd
import random
import os

def generate_dataset(num_records=1000, output_path="tickets.csv"):
    categories = ["Hardware", "Software", "Network", "Access/Security", "Billing"]
    priorities = ["Low", "Medium", "High", "Critical"]
    
    # Templates for ticket generation
    templates = {
        "Hardware": [
            {
                "subject": "Laptop won't power on",
                "desc": "My corporate laptop (ThinkPad) is not turning on when I press the power button. The charging light is on, but the screen remains black. I have a presentation in 2 hours, please help.",
                "priority": "Critical"
            },
            {
                "subject": "Swollen laptop battery",
                "desc": "I noticed today that the bottom case of my laptop is bulging. I think the battery is swollen. This seems dangerous and is a safety hazard, can I get a replacement immediately?",
                "priority": "High"
            },
            {
                "subject": "Broken screen on work laptop",
                "desc": "I accidentally dropped my laptop and the screen is cracked. It has lines running through it and I cannot use it. Need a screen replacement as soon as possible.",
                "priority": "High"
            },
            {
                "subject": "Monitor display issues",
                "desc": "My second monitor is not receiving any signal. I've tried unplugging and plugging back in the HDMI cable but it still says no signal. It was working fine yesterday.",
                "priority": "Medium"
            },
            {
                "subject": "HDMI port not working on dock",
                "desc": "The HDMI port on my docking station seems to have stopped working. I tested the cable on another device and it works fine, so it's definitely the dock.",
                "priority": "Medium"
            },
            {
                "subject": "External monitor flickering",
                "desc": "My external monitor has started flickering constantly today. It makes it impossible to work. I have tried rebooting my computer and updating drivers.",
                "priority": "Medium"
            },
            {
                "subject": "Requesting new keyboard and mouse",
                "desc": "I would like to request an ergonomic keyboard and mouse for my desk setup. My current keyboard has sticky keys and it causes hand fatigue.",
                "priority": "Low"
            },
            {
                "subject": "Headset microphone not working",
                "desc": "During Teams calls, my wireless headset microphone does not pick up my voice. The audio output works fine, but input is dead. I tried changing the input device in settings.",
                "priority": "Low"
            },
            {
                "subject": "Replacement charger needed",
                "desc": "I left my laptop charger in a hotel room last week. Can I request a replacement USB-C charger for my laptop? Currently running on low battery.",
                "priority": "Low"
            }
        ],
        "Software": [
            {
                "subject": "Excel crashes when opening large files",
                "desc": "Every time I try to open our monthly financial spreadsheet in Excel, the application freezes and crashes. It is a very large file containing lots of macros.",
                "priority": "High"
            },
            {
                "subject": "IDE license key expired",
                "desc": "My IntelliJ/PyCharm license key has expired today. I cannot run my code or do my work. Please provide a new license key so I can resume development.",
                "priority": "High"
            },
            {
                "subject": "Slack won't launch",
                "desc": "I click on the Slack icon but the app refuses to launch. I tried ending the task in Task Manager and restarting, but it didn't help. I am missing important notifications.",
                "priority": "Medium"
            },
            {
                "subject": "Docker container permission error",
                "desc": "I am getting a permission denied error when trying to run docker-compose up. It says it cannot bind to port 80. I've tried running with sudo but it still fails.",
                "priority": "Medium"
            },
            {
                "subject": "Need Adobe Acrobat Pro license",
                "desc": "I need to edit and sign a PDF document for a vendor contract. Can I get a license for Adobe Acrobat Pro installed on my machine? I need this by Friday.",
                "priority": "Medium"
            },
            {
                "subject": "Git merge conflict help",
                "desc": "I am having trouble resolving a complex merge conflict on git. I need help from someone in the dev team to make sure I don't lose changes on the release branch.",
                "priority": "Low"
            },
            {
                "subject": "Browser extension installation request",
                "desc": "I would like permission to install the Grammarly browser extension on Chrome. It says extension installation is blocked by the administrator.",
                "priority": "Low"
            }
        ],
        "Network": [
            {
                "subject": "VPN connection keeps disconnecting",
                "desc": "My Cisco AnyConnect VPN disconnects every 5 minutes. It says 'session timed out' or 'connection lost'. I am working from home and cannot get anything done.",
                "priority": "High"
            },
            {
                "subject": "Cannot access production database",
                "desc": "I am getting a connection timeout error when trying to connect to the production PostgreSQL database. I am connected to the VPN and my credentials are correct.",
                "priority": "High"
            },
            {
                "subject": "Entire office Wi-Fi is down",
                "desc": "None of our devices in the 4th-floor office can connect to the internal Wi-Fi. The network SSID is visible but authentication fails. We need this fixed urgently.",
                "priority": "Critical"
            },
            {
                "subject": "Slow internet speed in office",
                "desc": "The office internet is extremely slow today. Speed test shows less than 2 Mbps. Teams video calls are dropping and we can't open any web pages.",
                "priority": "Medium"
            },
            {
                "subject": "Unable to load internal wiki",
                "desc": "I am trying to access the internal Confluence wiki pages but I keep getting a 504 Gateway Timeout error. Is the server down? Other sites work fine.",
                "priority": "Medium"
            },
            {
                "subject": "Printers offline on network",
                "desc": "I cannot print to the office printer. It shows 'Printer Offline' on my computer. I checked the printer itself and it seems turned on and connected.",
                "priority": "Low"
            }
        ],
        "Access/Security": [
            {
                "subject": "Account locked after multiple login attempts",
                "desc": "I entered the wrong password too many times and now my Active Directory account is locked. Please unlock it so I can log in and start my shift.",
                "priority": "High"
            },
            {
                "subject": "Urgent: Reset MFA device",
                "desc": "I lost my phone which had my Google Authenticator app for MFA. I cannot log into my work account. Need to reset MFA device or set up a backup option.",
                "priority": "High"
            },
            {
                "subject": "Password reset required",
                "desc": "My password has expired and I cannot log into my work laptop. Please reset my password and send me a temporary one via SMS.",
                "priority": "High"
            },
            {
                "subject": "Access request for GitHub repository",
                "desc": "I need write access to the new frontend repo on GitHub. My github username is developer123. Can you add me to the repo?",
                "priority": "Medium"
            },
            {
                "subject": "Requesting folder permissions on shared drive",
                "desc": "I cannot access the Shared Marketing folder on the network drive. I get an Access Denied error. I need read/write access for the upcoming campaign.",
                "priority": "Medium"
            },
            {
                "subject": "Phishing email report",
                "desc": "I received an email pretending to be from the CEO asking for gift cards. I suspect it's a phishing email. Forwarding details to the security team.",
                "priority": "High"
            },
            {
                "subject": "Unauthorized access alert",
                "desc": "I received an alert of a login to my account from an unrecognized location/IP address in another country. Please check if my account has been compromised.",
                "priority": "Critical"
            },
            {
                "subject": "Lost office access badge",
                "desc": "I lost my physical office access card somewhere on my commute this morning. Please deactivate it and issue a new one so I can enter the building tomorrow.",
                "priority": "Medium"
            }
        ],
        "Billing": [
            {
                "subject": "Credit card declined on subscription",
                "desc": "Our monthly subscription payment was declined. The billing credit card is up to date. Please check why it failed to avoid service interruption.",
                "priority": "High"
            },
            {
                "subject": "Refund request for double charge",
                "desc": "I was charged twice for the software renewal this month. Please refund the duplicate charge of $120. I can provide the invoices.",
                "priority": "Medium"
            },
            {
                "subject": "Invoice dispute on pricing plan",
                "desc": "Our latest invoice has a higher amount than agreed. We were charged for 15 users instead of 10. Please adjust the invoice to the correct amount.",
                "priority": "Medium"
            },
            {
                "subject": "Requesting copy of invoice",
                "desc": "Can you please send me a PDF copy of the invoice for May 2026? It was not received by our accounting team. Need it for tax reporting.",
                "priority": "Low"
            },
            {
                "subject": "Update billing address",
                "desc": "We need to update our company billing address on all future invoices to our new office location in Chicago. The new address is 123 Main St, Chicago, IL.",
                "priority": "Low"
            },
            {
                "subject": "Questions about enterprise pricing",
                "desc": "We are considering upgrading from the Team plan to the Enterprise plan. Could you send details on pricing and volume discounts for 100+ seats?",
                "priority": "Low"
            }
        ]
    }
    
    # Random words/phrases to add variety
    departments = ["QA", "Marketing", "DevOps", "HR", "Sales", "Finance", "Product", "Support"]
    names = ["John Doe", "Jane Smith", "Alice Johnson", "Bob Brown", "Charlie Green", "Emily White", "David Black", "Fiona Grey"]
    devices = ["MacBook Pro", "Dell Latitude", "ThinkPad T14", "iPad Air", "iPhone 15"]
    os_systems = ["Windows 11", "macOS Sonoma", "Ubuntu 22.04", "Windows 10"]
    
    records = []
    
    # Generate balanced dataset
    for i in range(num_records):
        category = random.choice(categories)
        template = random.choice(templates[category])
        
        # Base templates
        subject = template["subject"]
        desc = template["desc"]
        priority = template["priority"]
        
        # Inject variations
        dept = random.choice(departments)
        name = random.choice(names)
        device = random.choice(devices)
        os_sys = random.choice(os_systems)
        ticket_id_num = 1000 + i
        
        # Contextual mutations
        mutations = [
            f" [User: {name} from {dept}]",
            f" I am using a {device} running {os_sys}.",
            f" This is affecting our entire {dept} team.",
            f" Please contact me at {name.lower().replace(' ', '.')}@company.com if you need more details.",
            ""
        ]
        
        # Add a random mutation to the description
        desc += random.choice(mutations)
        
        # Sometimes swap priority slightly based on random noise
        if random.random() < 0.15:
            priority = random.choice(priorities)
            
        records.append({
            "ticket_id": f"TKT-{ticket_id_num}",
            "subject": subject,
            "description": desc,
            "category": category,
            "priority": priority
        })
        
    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)
    print(f"Successfully generated {num_records} tickets and saved to {output_path}")

if __name__ == "__main__":
    # Get directory of this script to save tickets.csv there
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_dir, "tickets.csv")
    generate_dataset(1200, output_file)
