function Bird() {
  this.y = 300 * scaleFactor;
  this.x = 64 * scaleFactor;

  this.gravity = 0.7 * scaleFactor;
  this.lift = -12 * scaleFactor;
  this.velocity = -12 * scaleFactor;

  this.show = function() {
    fill(255);
    image(birdImg, this.x, this.y, 56 * scaleFactor, 48 * scaleFactor);
  };

  this.up = function() {
    this.velocity += this.lift;
    flapSound.play()
  };

  this.update = function() {
    this.velocity += this.gravity;
    // this.velocity *= 0.9;
    this.y += this.velocity;

    if (this.y > height - 79 * scaleFactor) {
      this.y = height - 79 * scaleFactor;
      this.velocity = 0;
    }

    if (this.y < 0) {
      this.y = 0;
      this.velocity = 0;
    }
  };
}
            