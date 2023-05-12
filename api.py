from steamship import check_environment, RuntimeEnvironments, Steamship
from steamship.invocable import post, PackageService


class PromptPackage(PackageService):
  # Modify this to customize behavior to match your needs.
  PROMPT = "You are now a gentle, all-knowing teacher. I am a 5 year old. Please explain {topic} to me, using descriptive and helpful metaphors where they are useful."

  @post("generate")
  def generate(self, topic: str) -> str:
    """Generate text from prompt parameters."""
    llm_config = {
      # Controls length of generated output.
      "max_words": 150,
      # Controls randomness of output (range: 0.0-1.0).
      "temperature": 0.3
    }
    prompt_args = {"topic": topic}

    llm = self.client.use_plugin("gpt-3", config=llm_config)
    return llm.generate(self.PROMPT, prompt_args)


if __name__ == "__main__":
  check_environment(RuntimeEnvironments.REPLIT)

  with Steamship.temporary_workspace() as client:
    prompt = PromptPackage(client)

    example_topic = "why is the sky blue"
    print("Ask me about any topic! Here's an example:")
    print("Topic: " + example_topic)
    print("Generating...")
    print("Explanation: " + prompt.generate(topic=example_topic))

    try_again = True
    while try_again:
      topic = input("What do you want to learn? There are no dumb questions! ")
      print("Generating...")
      print("Explanation: " + prompt.generate(topic))
      try_again = input("Generate another (y/n)? ").lower().strip() == 'y'
  
  print("See you next time, young scholar!")