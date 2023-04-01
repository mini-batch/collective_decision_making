from frontend.ExperimentScene import ExperimentScene

class SceneMananger():
    def __init__(self, environment):
        self.go_to(ExperimentScene(environment))

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self
