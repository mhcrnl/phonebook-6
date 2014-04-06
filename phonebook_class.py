import csv
import sys
from person import Person
from number_regex import clean_number

class Phonebook(object):
    def __init__(self, args):
        self.people = []
        self.filename = args.book
        if args.command != 'create':
            self.load_data()

    def create(self, params):
        filename = params[0]
        """
        Creates a new, empty phonebook file
        """
        # Check if file already exists to prevent accidental overwrites
        file_exists = True
        try:
            f = open(filename)
        except IOError:
            file_exists = False
        if file_exists:
            print ("Not created: file named %s already exists" % filename)
        else:
            self.filename = filename
            success_msg = ("Created phonebook named %s in the current directory." % filename)
            failure_msg = ("System error: failed to create phonebook named %s." % filename)
            self.save(success_msg, failure_msg)

 
    def lookup(self, params):
        search_name = params[0]
        """
        Looks up a person by name in an existing phonebook
        """
        output = ''
        for person in self.people:
            if search_name in person.name:
                person_string = person.name + " " + str(person.number)
                print person_string
                output = '\n'.join([output, person_string])
        if output == '':
            print "No entries found."

    def add(self, params):
        name = params[0]
        number = extract_number(params)
        person = Person(name, number)

        # make sure this won't be a duplicate
        if is_duplicate(person.name, self.people):
            print ("Entry not created: %s " % name) + \
                "is already in this phonebook."
            sys.exit()

        self.people.append(person)
        person_string = person.name + " " + str(person.number)
        success_msg = ("Entry '%s' added to phonebook %s" % (person_string, self.filename))
        failure_msg = "System error: failed to add person to phonebook."
        self.save(success_msg, failure_msg)


    def change(self, params):
        name = params[0]
        number = extract_number(params)
        
        if not is_duplicate(name, self.people):
            print ("%s is not in this phonebook. " % name) + \
                "Use 'add' instead."
            sys.exit()

        people_to_change = [p for p in self.people if p.name == name]
        person_to_change = people_to_change[0]
        if len(people_to_change) > 1:
            print ("There are multiple people named %s in %s" % (name, self.filename))
            sys.exit()

        old_number = person_to_change.number
        person_to_change.number = number
        success_msg =  "%s's phone number changed " % person_to_change.name + \
                       "from %s to %s." % (old_number, person_to_change.number)
        failure_msg = "System failure: failed to update number."
        self.save(success_msg, failure_msg)


    def remove(self, params):
        # Name requires an exact match, i.e. 'John' will not find 'John Smith'
        name = params[0]
        try:
            people_to_remove = [p for p in self.people if p.name == name]
            person_to_remove = people_to_remove[0]
        except IndexError:
            print "Cannot remove: there is no one in %s " % self.filename + \
                "named '%s'." % name
            sys.exit()
        self.people.remove(person_to_remove)
        success_msg = "Removed %s from %s." % (name, self.filename)
        failure_msg = "System failure: failed to remove %s from %s." % (name, self.filename)
        self.save(success_msg, failure_msg)

    def save(self, success_msg, failure_msg):
        try:
            self.execute_save()
            print success_msg
        except:
            print failure_msg
            sys.exit()

    def execute_save(self):
        # possible optimization: if adding a person,
        # just append to the file rather than rewriting
        # the entire thing
        with open(self.filename, 'wb') as f:
            fieldnames = ['name', 'number']
            csvwriter = csv.DictWriter(f, fieldnames)
            csvwriter.writerow(dict((fn, fn) for fn in fieldnames))
            for p in self.people:
                csvwriter.writerow(p.__dict__)

    def load_data(self):
        if not self.filename:
            print "Please include a phonebook filename."
            sys.exit()
        try:
            with open(self.filename, 'r') as f:
                reader = csv.DictReader(f)
                person_dicts = [row for row in reader]
            if person_dicts is not []:
                for person in person_dicts: 
                    p = Person.from_dict(person)
                    self.people.append(p)
        except IOError:
            print ('No file named %s found.' % self.filename)
            sys.exit()

def extract_number(params):
    """
    make sure number was included in input
    """
    try:
        number = clean_number(params[1])
    except IndexError:
        print "Please include a phone number."
        sys.exit()
    return number

def is_duplicate(name, people_list):
    already_in_book = [p.name for p in people_list]
    if name in already_in_book:
        return True

