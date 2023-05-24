import json
from mlflow.tracking import MlflowClient
from mlflow.sklearn import load_model
import mlflow
import os

import pickle
import sys
import random



def get_mlflow_client():
    return MlflowClient()


def log_dataset(df, artefact_name):
    filename = f'{artefact_name}.pkl'
    df.to_pickle(filename)
    mlflow.log_artifact(filename, artifact_path='datasets')


def log_dataset_analysis_profile(df, report_name):
    profile = df.profile_report(title=report_name, style={'full_width': True})
    report_file = "{}_profile_analysis.html".format(report_name)
    profile.to_file(output_file=report_file)
    mlflow.log_artifact(report_file, artifact_path='analysis')


def log_plt_visualisation(fig_obj, visualisation_name):
    filename = f'{visualisation_name}.png'
    fig_obj.savefig(filename)
    mlflow.log_artifact(filename, artifact_path='visualisations')


def log_predict_features(predict_features):
    pred_features_filename = 'predict_features.json'
    with open(pred_features_filename, 'w') as json_file:
        pred_features = {'feature_names': predict_features}
        json.dump(pred_features, json_file)
    mlflow.log_artifact(pred_features_filename, artifact_path='features')


def log_features(feature_list, file_name='predict_features.json'):
    features = {'feature_names': feature_list}
    mlflow.log_text(json.dumps(features), 'features/' + file_name)


def log_reasons(reasons_list, file_name='reasons.json'):
    reasons = {'reasons': reasons_list}
    mlflow.log_text(json.dumps(reasons), 'reasons/' + file_name)


def log_explanations(reasons, description, modelbook):
    mlflow.log_text(reasons, 'explanations/reasons.txt')
    mlflow.log_text(description, 'explanations/description.txt')
    mlflow.log_text(modelbook, 'explanations/modelbook.txt')


def model_size_mb(model):
    return sys.getsizeof(pickle.dumps(model)) / 1024 / 1024


class MLFlowConfigurationError(Exception):
    pass


def get_runs_for(application_name, variant_name):
    """
    Retrieves the mlflow run records for a given application and flow name
    :param application_name: the ML application name (mlflow experiment name). Eg. `bank_account`
    :param variant_name: the flow name or use case within the application domain.  For example `outlier_model`
    :return: the mlflow run records as a  pandas dataframe
    """
    experiment = mlflow.get_experiment_by_name(application_name)
    if experiment:
        training_runs = mlflow.search_runs(experiment.experiment_id)
        training_flow_runs = training_runs[training_runs['tags.variant_name'] == variant_name]
        return training_flow_runs
    else:
        raise ValueError(f'No experiment existing with name: {application_name}')


def get_next_model_id_for(application_name, flow_name):
    """
    Return the next model version id for a given application and flow
    :param application_name: the ML application name (mlflow experiment name). Eg. `bank_account`
    :param flow_name: the flow name or use case within the application domain.  For example `outlier_model`
    :return: a sequence value
    """
    training_flow_runs = get_runs_for(application_name, flow_name)
    max_model_version = training_flow_runs['model_version'].astype(
        int).max() if 'model_version' in training_flow_runs.columns else 0
    next_model_id = max(len(training_flow_runs), max_model_version) + 1
    return next_model_id


def replay_model_versions_for(application_name, flow_name):
    """
    Retrieves all mlflow records for the givne application and flow name and updates the model_version based on the
    order of run_label
    :param application_name:
    :param flow_name:
    :return: the mlflow run records with the updated tags.model_version values
    """
    training_flow_runs = get_runs_for(application_name, flow_name)
    if len(training_flow_runs) > 0:
        training_flow_runs = training_flow_runs.sort_values('params.run_label')
        for v, run_data in enumerate(training_flow_runs.to_dict(orient='records')):
            with mlflow.start_run(run_data['run_id']) as run:
                mlflow.set_tag('model_version', v + 1)
    return get_runs_for(application_name, flow_name)


creatures = [
    'monkey', 'panda', 'shark', 'zebra', 'gorilla', 'walrus', 'leopard', 'wolf', 'antelope',
    'eagle', 'jellyfish', 'crab', 'giraffe', 'woodpecker', 'camel', 'starfish', 'koala',
    'lion', 'crocodile', 'dolphin', 'elephant', 'squirrel', 'snake', 'kangaroo', 'hippopotamus',
    'elk', 'rabbit', 'fox', 'gorilla', 'bat', 'hare', 'toad', 'frog', 'deer', 'rat', 'badger',
    'lizard', 'mole', 'hedgehog', 'otter', 'reindeer', 'yak', 'flamingo', 'unicorn', 'zealot',
    'hydralisk', 'griffin', 'pangolin', 'rhino', 'slug', 'dungbeetle', 'owl', 'terrier',
    'spider', 'catfish', 'albatross', 'puffin', 'impala', 'mantis', 'turtle', 'tortise',
    'aphid', 'centipede', 'millipede', 'dragon', 'princess', 'elf', 'leopard', 'baboon', 'hyena',
    'lobster', 'shrimp', 'krill', 'squid', 'snail', 'worm', 'butterfly', 'tadpole',
    'insect', 'gibbon', 'lemur', 'hamster', 'bunny', 'chinchilla', 'mongoose', 'fairy',
    'dwarf', 'orc', 'hobbit', 'wizard', 'witch', 'alchemist', 'warlock', 'enchantress',
    'hippogriff', 'cheetah', 'bear', 'wombat', 'iguana', 'cormorant', 'sloth', 'piranha',
    'platypus', 'stork', 'armadillo', 'anteater', 'wasp', 'hornet', 'seahorse', 'manatee',
    'narwhal', 'moose', 'caribou'
]

adj_verbs = [
    'shaking', 'leaping', 'singing', 'miming', 'sombre', 'thinking', 'ravenous', 'shrieking',
    'laughing', 'fearful', 'brave', 'contemplative', 'forgotten', 'appointed', 'calm', 'drunk',
    'diligent', 'powerful', 'energised', 'fiesty', 'grumpy', 'ecstatic', 'sleeping', 'shaving',
    'inebriated', 'intoxicated', 'running', 'sprinting', 'diving', 'charging', 'exploding',
    'trumpeting', 'drumming', 'reigning', 'amnesic', 'narcoleptic', 'dozing', 'apoplectic',
    'sanguine', 'jazzy', 'delicate', 'lumbering', 'skittish', 'snoring', 'lethargic',
    'over-weight', 'doleful', 'skuttling', 'friendly', 'frolicking', 'howling', 'hooting', 'barking',
    'rampant', 'yodelling', 'winking', 'nodding', 'blinking', 'dashing', 'waltzing', 'rolling',
    'swimming', 'abandonned', 'analytical', 'logical', 'illogical', 'swarming', 'noodling',
    'mathematical', 'investigating', 'fantastical', 'gymnastic', 'mystical', 'complicated',
    'intuitive', 'charismatic', 'charming', 'flexible'
]

nums = list(range(10))

def get_random_name():
    """
    generates a random name for use as a human friendly handle to model instances
    """
    return random.choice(adj_verbs) + '-' + random.choice(creatures) + f": {random.choice(nums)}"

######

def get_run(experiment_name, model_id):
    experiment = mlflow.get_experiment_by_name(experiment_name)
    filter_string = f"tags.model_id = '{model_id}'"
    return mlflow.search_runs(experiment.experiment_id, filter_string).head()


def get_model_artefacts_uri(experiment_name, model_id):
    run = get_run(experiment_name, model_id)
    return run.artifact_uri.values[0]


def get_flow_name(experiment_name, model_id):
    run = get_run(experiment_name, model_id)
    return run['tags.flow_name'].values[0]

#
# def parse_s3_uri(s3_path):
#     bucket, key = s3_path.replace("s3://", "").split("/", maxsplit=1)
#     return bucket, key
#
#
# def artifact_exists(s3_path):
#     s3 = boto3.client('s3')
#     bucket, key = parse_s3_uri(s3_path)
#     response = s3.list_objects(Bucket=bucket, Prefix=key)
#     if response:
#         if 'Contents' in response:
#             return True
#
#     return False
#
#
# def get_artifact_from_s3(s3_path):
#     s3 = boto3.resource('s3')
#     bucket, key = parse_s3_uri(s3_path)
#     obj = s3.Object(bucket, key)
#     return obj.get()['Body'].read().decode('utf-8')
#
#
# def get_json_from_s3(s3_path, default=None):
#     if artifact_exists(s3_path):
#         artifact = get_artifact_from_s3(s3_path)
#         return json.loads(artifact)
#     else:
#         if not default:
#             raise ValueError(f"Artifact {s3_path} does not exist.")
#         else:
#             return default
#
#
# def features_and_explanations(experiment_name, model_id):
#     artefacts_uri = get_model_artefacts_uri(experiment_name, model_id)
#
#     artifacts = {
#         'feature_names': get_json_from_s3(f'{artefacts_uri}/features/predict_features.json')['feature_names'],
#         'reasons': get_text_from_s3(f'{artefacts_uri}/explanations/reasons.txt'),
#         'description': get_text_from_s3(f'{artefacts_uri}/explanations/description.txt'),
#         'name': get_flow_name(experiment_name, model_id)
#     }
#
#     return artifacts
#
#
# def get_supporting_artifacts(experiment_name, model_id):
#     artefacts_uri = get_model_artefacts_uri(experiment_name, model_id)
#
#     artifacts = {
#         'predict_features': get_json_from_s3(f'{artefacts_uri}/features/predict_features.json')['feature_names'],
#         'filtering_features':
#             get_json_from_s3(f'{artefacts_uri}/features/filtering_features.json', default={'feature_names': []})[
#                 'feature_names'],
#         'reasons': get_artifact_from_s3(f'{artefacts_uri}/explanations/reasons.txt'),
#         'description': get_artifact_from_s3(f'{artefacts_uri}/explanations/description.txt'),
#         'name': get_flow_name(experiment_name, model_id)
#     }
#
#     artifacts['preprocessing_features'] = artifacts['predict_features'] + artifacts['filtering_features']
#
#     return artifacts



