import os
from datetime import datetime
from.config import OUTPUTS_DIR
def create_session_folder():
    session_id=datetime.now().strftime("%Y%m%d_%H%M%S")
    session_path=os.path.join(OUTPUTS_DIR,session_id)
    os.makedirs(session_path,exist_ok=True)
    os.makedirs(os.path.join(session_path,"multiview"),exist_ok=True)
    return session_id,session_path