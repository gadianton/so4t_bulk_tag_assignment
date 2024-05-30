# Native Python libraries
import argparse
import json

# Local libraries
from so4t_api_v3 import V3Client

# Third-party libraries


def main():

    args = get_args()
    if not args.url or not args.token or not args.tag:
        print("--------------------")
        print("Missing required arguments.")
        print("Please make sure to provide a URL, token, and tag.")
        print("See the README file for additional instructions.")
        print("--------------------")
        return

    client = V3Client(args.url, args.token)

    questions = client.get_all_questions()
    questions_with_max_tags = add_tag_to_questions(client, questions, args.tag)

    print("***********")
    if questions_with_max_tags:
        print("Some questions already had the maximum amount of tags (i.e. five)")
        print("The list of those questions has been written to `questions_with_max_tags.json`")
        export_to_json('questions_with_max_tags', questions_with_max_tags)
    else:
        print("All questions were successfully updated!")
 

def get_args():

    parser = argparse.ArgumentParser(
        prog='main.py',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('--url', help='The URL of the Stack Overflow for Teams site')
    parser.add_argument('--token', help='Your access token for the Stack Overflow API')
    parser.add_argument('--tag', help='The tag to be added to all questions')
    # Could add an optional argument to pass in a list of question IDs

    return parser.parse_args()


def add_tag_to_questions(client, questions, new_tag):

    questions_with_max_tags = []
    for question in questions:
        
        question_id = question['id']
        title = question['title']
        body = question['body']

        # The API for questions provides full tag objects instead of just tag names, 
        # so we need to extract the name from each tag object
        tags = []
        for tag in question['tags']:
            tags.append(tag['name'])

        if new_tag in tags:
            print(f"Question {question_id} already has the tag '{new_tag}'. Skipping...")
            continue
        else:
            tags.append(new_tag)
        
        if len(tags) > 5:
            print(f"Question {question_id} has too many tags and cannot be edited.")
            questions_with_max_tags.append(question['shareUrl'])
            continue
        
        print(f"Updating question with ID {question_id}...")
        response = client.edit_question(question_id, title, body, tags)
        print(f"... question updated successfully!")

    return questions_with_max_tags


def export_to_json(file_name, data):

    with open(file_name + '.json', 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":

    main()